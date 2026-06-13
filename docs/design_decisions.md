# Design Decisions

This document records the significant engineering choices behind the toolchain
and the trade-offs each one makes.

---

## Recursive-descent parsing

**Decision.** The Jack frontend uses a hand-written recursive-descent parser:
one function per grammar production, with the call graph mirroring the grammar.

**Why.**
- **Direct correspondence to the grammar.** `compile_class`, `compile_subroutine`,
  `compile_statement`, `compile_expression`, and `compile_term` read as an
  executable transcription of the language specification. A reviewer can check the
  parser against the grammar production by production.
- **Predictive, single-token lookahead.** The Jack grammar is `LL(1)` at almost
  every point; the one ambiguous case — an identifier that may begin a variable
  reference, an array access, or a subroutine call — is resolved with a single
  peek at the next token. No backtracking is needed.
- **Precise error reporting.** Because each method knows exactly what it expects,
  a mismatch can name the expected token, the actual token, and its position.
- **No generator dependency.** A hand-written parser keeps the project free of a
  parser-generator toolchain and keeps the generated-vs-source mapping explicit.

**Trade-off.** Recursive descent cannot directly express left-recursive grammars
and is less suited to highly ambiguous languages, where a table-driven `LR`
parser would scale better. For Jack's small, deliberately regular grammar, the
clarity of recursive descent wins.

---

## Symbol-table design

**Decision.** Two separate tables — one **class-level**, one
**subroutine-level** — each mapping a name to a `(type, kind, index)` triple,
with a per-kind running counter.

**Why.**
- The `(type, kind, index)` triple is exactly what code generation needs: the
  **kind** selects the VM memory segment, the **index** is the offset within it,
  and the **type** drives method dispatch on objects.
- Per-kind counters assign indices densely and in declaration order, which is
  precisely the layout the VM segments expect.
- Keeping the two scopes in distinct tables makes scope reset trivial (see below)
  and keeps class state isolated from subroutine state.

**Trade-off.** Two flat tables model exactly two scope levels. A language with
nested block scopes would need a scope stack instead. Jack has no nested scopes,
so two tables are sufficient and simpler.

---

## Scope management

**Decision.** Lookups consult the subroutine table first and fall back to the
class table; the subroutine table (and its argument/local counters) is reset at
the start of every subroutine, while the class table persists for the whole
class.

**Why.**
- **First-match lookup implements shadowing for free.** A local or argument with
  the same name as a field is found first, so it correctly shadows the field.
- **Resetting per subroutine** guarantees that argument and local indices restart
  at zero for each routine, matching the fresh `argument`/`local` segments each
  call frame receives.
- **Methods reserve argument 0 for `this`.** Defining the implicit `this`
  argument first makes object-relative field access fall out naturally.

**Trade-off.** This hard-codes a two-level scope policy. It is the right amount of
machinery for the language and avoids the overhead of a general scope stack.

---

## The VM abstraction layer

**Decision.** Compile to a stack-based virtual-machine IR rather than emitting
assembly directly from the language frontend.

**Why.**
- **Separation of concerns.** The frontend reasons only about language semantics;
  the backend reasons only about the machine. Neither has to understand the
  other.
- **Retargetability.** A new source language reuses the entire backend by
  emitting VM code; a new hardware target reuses the entire frontend by writing a
  new VM translator. The IR is the contract between the two halves.
- **A simpler code-generation target.** A stack machine has no register
  allocation problem: every intermediate value lives on the stack. This makes the
  frontend's code generator dramatically simpler than one targeting registers
  directly.

**Trade-off.** The extra layer costs one translation pass and produces less
efficient code than direct, register-aware generation. For a teaching-scale stack
the modularity is worth far more than the lost cycles — the same reasoning that
justifies an IR in production compilers like LLVM.

---

## Code-generation strategy

**Decision.** Generate VM code **during** the parse (syntax-directed translation),
rather than building an AST and walking it in a separate phase.

**Why.**
- **Single pass, low overhead.** Jack requires no whole-program analysis or
  optimization, so there is nothing that needs a materialized tree to inspect.
- **Less machinery.** No AST node types, no tree-walking visitor — the parser's
  own recursion is the traversal, and code is emitted at the natural point in
  each production.
- **Expressions fall out as postfix.** Emitting operands before operators yields
  exactly the stack order the VM expects, so expression compilation is a direct
  consequence of the parse order.

**Trade-off.** Without an AST there is no convenient place to run global
optimizations or multi-pass analyses. Those are explicit non-goals here; if they
became goals, an AST phase would be inserted between parsing and generation
without disturbing the other stages.

---

## Memory-segment mapping

**Decision.** Map the VM's eight logical segments onto fixed regions of Hack RAM,
with pointer-relative addressing for the dynamic segments.

**Why.**
- **`local`, `argument`, `this`, `that`** are addressed relative to the pointers
  `LCL`, `ARG`, `THIS`, `THAT`, so each call frame and each object transparently
  gets its own view of these segments.
- **`pointer`** writes `THIS`/`THAT` directly, which is how a constructor sets the
  base of the current object and how array access rebases `that`.
- **`temp`** occupies the fixed scratch registers `R5`–`R12`; **`static`** is
  realized as per-file assembler symbols so statics are unique per class but
  shared across a class's subroutines; **`constant`** is virtual and read-only.

**Trade-off.** A fixed mapping is fast and trivial to reason about but assumes the
specific Hack memory layout. Retargeting to another machine means re-choosing the
mapping — which is exactly the VM translator's job, and exactly why that decision
lives in the backend rather than the frontend.
