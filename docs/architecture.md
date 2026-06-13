# Architecture

This document describes the system as a layered compiler: a **frontend** that
understands the source language, a **middle-end** that defines a
platform-independent intermediate representation, and a **backend** that lowers
that representation to a concrete machine. It then describes the **runtime
model**, the **memory model**, and the role of the **VM abstraction layer** that
holds the whole stack together.

```
   Source language  ─────────────────────────────▶  Hardware
        Jack            frontend │ middle-end │ backend      Hack CPU
```

---

## Frontend — the Jack compiler

The frontend ([`jack_compiler/`](../jack_compiler/)) turns Jack source text into
intermediate code. It is organized as a classic compiler frontend:

1. **Lexical analysis** (`JackTokenizer.py`). The source is scanned into a flat
   token stream. The scanner strips line and block comments while respecting
   string literals, then classifies each token as a keyword, symbol, identifier,
   integer constant, or string constant. This stage erases formatting and
   commentary so later stages see only meaningful tokens.

2. **Syntactic analysis** (`CompilationEngine.py`). A recursive-descent parser
   consumes the token stream. Each non-terminal in the Jack grammar
   (`class`, `subroutineDec`, `statement`, `expression`, `term`, …) maps to one
   method. The parser validates that the token stream conforms to the grammar
   and drives every downstream action.

3. **Semantic analysis** (`SymbolTable.py`). As declarations are parsed, the
   symbol table records each identifier's **kind** (static, field, argument,
   local), **type**, and **index**. Name references are resolved against this
   table to determine which memory segment and offset they denote. This is where
   the compiler enforces and exploits the language's scoping rules.

4. **Code generation** (`VMWriter.py`, invoked from the engine). The frontend
   emits VM intermediate code directly during the parse, rather than building and
   then walking a separate syntax tree. Expressions compile to stack operations;
   statements compile to stack manipulation and control-flow commands.

The frontend's only output contract is a stream of VM commands. It knows nothing
about registers, instruction encodings, or the hardware below it.

---

## Middle-end — the VM intermediate representation

The middle layer is the **stack-based virtual machine** specification. It is the
project's central abstraction: a small, platform-independent instruction set
that is simultaneously the frontend's output target and the backend's input.

The VM offers:
- a single **operand stack** for all computation,
- nine arithmetic/logical commands (`add`, `sub`, `neg`, `eq`, `gt`, `lt`,
  `and`, `or`, `not`),
- two memory commands (`push` / `pop`) over eight named segments,
- three control-flow commands (`label`, `goto`, `if-goto`), and
- three function commands (`function`, `call`, `return`).

Because the IR is defined independently of both the source language and the
target machine, it is the seam along which the stack can be retargeted: a new
source language only needs to emit VM code, and a new hardware target only needs
a new VM translator.

---

## Backend — VM translator and assembler

The backend lowers the IR to executable machine code in two stages.

### VM translator ([`vm_translator/`](../vm_translator/))
Translates the **stack machine** onto a **register/memory machine**. The Hack
CPU has no hardware stack, so the translator synthesizes one in RAM using the
`SP` pointer and emits the explicit pointer arithmetic for every push, pop, and
arithmetic operation. It also realizes the function-call ABI (see *Runtime
model*) and lowers VM branches to assembly jumps. Its parser
(`parser.py`) classifies VM commands; its `code_writer.py` emits the
corresponding assembly templates.

### Assembler ([`assembler/`](../assembler/))
Translates symbolic Hack assembly into 16-bit binary in two passes:
- **Pass one** walks the program counting real instructions and records the ROM
  address of every label `(LOOP)` in the symbol table.
- **Pass two** re-walks the program, allocates RAM addresses for new variables
  (starting at address 16), resolves every symbol, and encodes each A- and
  C-instruction into its 16-bit word.

Separating the two passes is what allows forward references (a jump to a label
defined later) to resolve cleanly.

---

## Runtime model

The runtime is defined by the VM's function-calling convention, implemented by
hand in the VM translator.

**On `call f n`:**
1. The return address is pushed.
2. The caller's segment pointers `LCL`, `ARG`, `THIS`, `THAT` are pushed.
3. `ARG` is repositioned to point at the first of the `n` arguments already on
   the stack (`ARG = SP - 5 - n`).
4. `LCL` is set to the current stack top, establishing the callee's frame.
5. Control jumps to `f`.

**On `function f k`:** the label is emitted and `k` local slots are pushed and
zero-initialized.

**On `return`:**
1. The frame base (`LCL`) is saved; the return address is read from a fixed
   offset within the saved frame.
2. The return value is copied into `ARG[0]`, and `SP` is reset just above it, so
   the result replaces the arguments on the caller's stack.
3. `THAT`, `THIS`, `ARG`, `LCL` are restored from the saved frame.
4. Control jumps to the recovered return address.

Program execution begins at the **bootstrap** the translator emits when given a
directory: `SP` is initialized to 256 and `Sys.init` is called.

---

## Memory model

The VM exposes eight logical segments, which the backend maps onto Hack RAM:

| Segment     | Backed by            | Meaning                                   |
|-------------|----------------------|-------------------------------------------|
| `local`     | `LCL`-relative       | a subroutine's local variables            |
| `argument`  | `ARG`-relative       | a subroutine's arguments                  |
| `this`      | `THIS`-relative      | fields of the current object              |
| `that`      | `THAT`-relative      | array / heap element access               |
| `pointer`   | `THIS` / `THAT`      | sets the base of `this` / `that`          |
| `temp`      | RAM 5–12             | scratch space                             |
| `static`    | per-file labels      | class-level static variables              |
| `constant`  | (virtual)            | literal values; read-only                 |

The low RAM addresses hold the machine's fixed registers (`SP=0`, `LCL=1`,
`ARG=2`, `THIS=3`, `THAT=4`), with `R5`–`R15` as general scratch. The stack grows
upward from address 256; the heap and the memory-mapped screen and keyboard sit
in the high address range. Objects are allocated on the heap, with `THIS`
pointing at the current instance and `pointer 0`/`pointer 1` rebasing the `this`
and `that` segments.

---

## VM abstraction layer

The virtual machine is the architectural keystone. It cleaves a single, tightly
coupled "language to hardware" problem into two independent, well-specified
problems:

- **Frontend ↔ VM.** The Jack compiler targets the VM, not the CPU. Adding a new
  source language means writing a new frontend that emits the same VM code; the
  entire backend is reused unchanged.
- **VM ↔ Hardware.** The VM translator targets one CPU. Porting the stack to a
  different machine means writing a new translator; the entire frontend is reused
  unchanged.

This is the same layering that lets real toolchains share a backend across
languages (as LLVM IR does) and share a frontend across targets. Here it is
realized in miniature, with both halves fully implemented, so the benefit of the
intermediate representation is visible end to end.
