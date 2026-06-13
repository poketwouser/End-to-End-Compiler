# Compiler Pipeline

This is a pass-by-pass walk-through of how a program descends from Jack source to
the binary words a CPU executes. Each section names the responsible module and
shows the representation entering and leaving that pass.

```
Jack source → Tokenizer → Parser → Semantic Analysis → VM Generation
            → VM Translator → Assembly → Assembler → Machine Code → Hardware
```

We trace a single fragment through the stack:

```jack
let x = a + 1;
```

assuming `x` and `a` are local variables (indices 0 and 1).

---

## 1. Lexical analysis — `jack_compiler/JackTokenizer.py`

**In:** raw source text. **Out:** a token stream.

Comments and whitespace are removed (string literals are preserved verbatim), and
the remaining characters are grouped into classified tokens:

```
keyword(let) identifier(x) symbol(=) identifier(a) symbol(+) integerConstant(1) symbol(;)
```

The scanner is a single left-to-right pass that recognizes the longest valid
token at each position.

---

## 2. Syntactic analysis — `jack_compiler/CompilationEngine.py`

**In:** token stream. **Out:** validated grammar structure, consumed top-down.

A recursive-descent parser matches the token stream against the Jack grammar.
`compile_let` recognizes the `let` statement; it calls `compile_expression`,
which calls `compile_term` for each operand. The parser confirms the fragment is
a well-formed `letStatement` and controls the order in which code is generated.

---

## 3. Semantic analysis — `jack_compiler/SymbolTable.py`

**In:** identifiers from the parse. **Out:** resolved segment + index per name.

Each identifier is looked up in the symbol table. `x` and `a` resolve to the
`local` segment at indices 0 and 1. The lookup also yields their type and kind,
which determine how they are read and written. Subroutine scope is consulted
before class scope, so locals correctly shadow fields.

---

## 4. VM code generation — `jack_compiler/VMWriter.py`

**In:** resolved expression structure. **Out:** stack-based VM code.

Expressions are emitted in postfix order: operands are pushed, then the operator
is applied to the stack top. The assignment pops the result into the target
variable.

```vm
push local 1     // a
push constant 1  // 1
add              // a + 1
pop local 0      // x = ...
```

This VM code is the frontend's final product and the backend's input.

---

## 5. VM translation — `vm_translator/` (`parser.py`, `code_writer.py`)

**In:** VM code. **Out:** Hack assembly.

The translator synthesizes the operand stack in RAM. Each VM command expands to
the explicit pointer arithmetic the CPU requires. For example, `add` pops the top
two stack cells, sums them, and pushes the result:

```asm
@SP
AM=M-1   // SP--, point at top operand
D=M      // D = top
A=A-1    // point at second operand
M=D+M    // second = second + top   (result left on stack)
```

`push local 1` becomes the computation of `LCL + 1`, a load from that address,
and a push onto the stack. Function calls expand into the full frame setup and
teardown described in [architecture.md](architecture.md#runtime-model).

---

## 6. Assembly — `assembler/` (`parser.py`, `code_module.py`, `symbol_table.py`)

**In:** symbolic Hack assembly. **Out:** 16-bit binary machine code.

The assembler runs two passes. Pass one records label addresses; pass two
resolves symbols, allocates RAM for variables, and encodes each instruction. A
C-instruction such as `M=D+M` is encoded field by field:

```
1 1 1  a c1 c2 c3 c4 c5 c6  d1 d2 d3  j1 j2 j3
1 1 1  1  0  0  0  0  1  0   0  0  1   0  0  0   →  1111000010001000
```

The `comp` bits come from the operation, the `dest` bits from the assignment
target, and the `jump` bits from any jump condition.

---

## 7. Hardware execution — `hardware/`

**In:** 16-bit machine code loaded into instruction ROM. **Out:** state changes
in RAM and on the screen.

The gate-level CPU fetches each 16-bit word and executes it. The ALU
([`hardware/alu/`](../hardware/alu/)) computes the C-instruction's `comp` field;
the register and RAM components ([`hardware/sequential/`](../hardware/sequential/),
[`hardware/memory/`](../hardware/memory/)) hold and update program state. The
high-level `let x = a + 1` has now become a physical sequence of gate
activations.

---

## Summary

| Stage | Module | Input | Output |
|-------|--------|-------|--------|
| Lexing | `JackTokenizer.py` | source text | tokens |
| Parsing | `CompilationEngine.py` | tokens | grammar structure |
| Semantic analysis | `SymbolTable.py` | identifiers | segment + index |
| VM generation | `VMWriter.py` | expressions | VM code |
| VM translation | `vm_translator/` | VM code | Hack assembly |
| Assembly | `assembler/` | assembly | machine code |
| Execution | `hardware/` | machine code | program state |
