# End-to-End Compiler and Systems Stack

![CI](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)

> Replace `USER/REPO` in the badge URL above once the repository is pushed to GitHub.

A complete, working compilation toolchain — from an object-oriented high-level
language down to the binary words executed by a gate-level CPU. Every layer of
the stack is implemented from scratch: the language frontend, the intermediate
virtual-machine, the backend code generators, and the digital logic that
ultimately runs the program.

The project demonstrates the full lifecycle of a program as it descends through
the abstraction boundaries of a real system:

```
   Jack source            (high-level, object-oriented language)
        │   Tokenizer + Recursive-Descent Parser + Symbol Table
        ▼
   VM intermediate code   (stack-based, platform-independent IR)
        │   VM Translator  (stack machine → register machine)
        ▼
   Hack assembly          (symbolic machine language)
        │   Assembler      (two-pass, symbol resolution)
        ▼
   Hack machine code       (16-bit binary instructions)
        │   loaded into ROM
        ▼
   Hardware (ALU / RAM / sequential logic)  — executes the program
```

Each arrow is a compiler pass implemented in this repository. The result is a
self-contained vertical slice of a computer system that makes the
language-to-hardware boundary concrete.

---

## Compiler Pipeline

```
 ┌────────────────────────────────────────────────────────────────────────┐
 │                            FRONTEND  (jack_compiler/)                    │
 │                                                                          │
 │   Jack source ──▶ Tokenizer ──▶ Recursive-Descent Parser ──▶ Semantic    │
 │                   (lexer)        (grammar-driven)             Analysis    │
 │                                                              (Symbol      │
 │                                                               Table,      │
 │                                                               scope)      │
 │                                          │                                │
 │                                          ▼                                │
 │                                    VM Code Generation                     │
 └──────────────────────────────────────────┬───────────────────────────────┘
                                             ▼
                                    VM intermediate code
                                             │
 ┌───────────────────────────────────────────┴──────────────────────────────┐
 │                            BACKEND  (vm_translator/, assembler/)           │
 │                                                                            │
 │   VM code ──▶ VM Translator ──▶ Hack assembly ──▶ Assembler ──▶ Machine    │
 │               (stack → reg)                       (two-pass)      code     │
 └────────────────────────────────────────────────────────────────┬─────────┘
                                                                    ▼
 ┌──────────────────────────────────────────────────────────────────────────┐
 │                            HARDWARE  (hardware/)                           │
 │   ALU · signed multiplier · adders · registers · RAM hierarchy · counter  │
 └──────────────────────────────────────────────────────────────────────────┘
```

A narrative walk-through of every pass is in
[docs/compiler_pipeline.md](docs/compiler_pipeline.md).

---

## Major Components

### Hardware Layer — [`hardware/`](hardware/)
Gate-level definitions (HDL) for the datapath that executes compiled programs:
- **`alu/`** — the Arithmetic Logic Unit, including a multiply path.
- **`arithmetic/`** — signed multiplier, carry-save adder, and carry-lookahead
  adder demonstrating different speed/area trade-offs.
- **`memory/`** — a RAM hierarchy built up from a single bit to a 16K word store.
- **`sequential/`** — the clocked primitives (bit, register, program counter)
  that give the machine state.

### Assembler — [`assembler/`](assembler/)
A two-pass assembler translating symbolic Hack assembly into 16-bit machine
code. Pass one resolves label addresses; pass two allocates variables and emits
binary. Mirrors a production assembler's separation of parsing, symbol
resolution, and code emission.

### VM Translator — [`vm_translator/`](vm_translator/)
Lowers a **stack-based** intermediate representation onto a **register/memory**
machine. Handles the function-call ABI (frame setup, argument/local segments,
caller/callee save and restore), the eight virtual memory segments, and
structured control flow (`label` / `goto` / `if-goto`).

### Jack Compiler — [`jack_compiler/`](jack_compiler/)
A full compiler frontend for **Jack**, an object-oriented language with classes,
constructors, methods, fields, static variables, arrays, and strings:
- **`JackTokenizer.py`** — lexical analysis.
- **`CompilationEngine.py`** — a recursive-descent parser fused with code
  generation.
- **`SymbolTable.py`** — two-level (class / subroutine) scope resolution.
- **`VMWriter.py`** — emits VM intermediate code.
- **`JackCompiler.py`** — the driver that ties the stages together.

---

## Key Features

- **Lexical analysis** — comment stripping, string handling, and tokenization of
  keywords, symbols, identifiers, and integer/string constants.
- **Recursive-descent parsing** — one parse routine per grammar production,
  giving a parser whose structure mirrors the language grammar.
- **Symbol-table management** — class-level and subroutine-level tables with
  kind, type, and running index per identifier.
- **Scope resolution** — subroutine scope shadows class scope; the table resets
  per subroutine while preserving class state.
- **Object-oriented compilation** — constructors (`Memory.alloc`), methods
  (implicit `this` argument), fields, and static members.
- **Function-call translation** — full calling convention: return address,
  saved segment pointers, argument/local frame layout, and teardown on return.
- **Memory-segment management** — `local`, `argument`, `this`, `that`,
  `constant`, `static`, `pointer`, and `temp` mapped onto physical RAM.
- **Control-flow translation** — high-level `if`/`while` lowered to VM
  branches, then to assembly jumps.
- **Machine-code generation** — symbolic assembly resolved to 16-bit binary.

---

## Design Highlights

- **Clean abstraction boundaries.** The VM layer decouples the language frontend
  from the target hardware. The Jack compiler never reasons about registers; the
  assembler never reasons about objects. New languages or targets can be added at
  the boundaries without touching the middle.
- **Grammar-driven frontend.** The parser is a direct, readable transcription of
  the Jack grammar, which keeps it auditable and easy to extend with new syntax.
- **Code generation interleaved with parsing.** Rather than building a full AST,
  the compilation engine emits VM code as it parses — a single-pass strategy that
  is simple, fast, and sufficient for the language.
- **Explicit calling convention.** The function-call ABI is implemented by hand
  in the VM translator, making the normally invisible mechanics of a stack frame
  fully concrete.

The reasoning behind these choices is documented in
[docs/design_decisions.md](docs/design_decisions.md), and the layered
architecture is described in [docs/architecture.md](docs/architecture.md).

---

## Example Usage

No third-party dependencies — Python 3.8+ and the standard library only.

### One command: Jack all the way to machine code

[`pipeline.py`](pipeline.py) chains all three backend stages and then verifies
the result like a linker would — every VM function that gets called must be
defined, and every emitted word must be valid 16-bit binary:

```bash
python pipeline.py examples/complete_program
```
```
Building 'complete_program' from 6 Jack source file(s)

[1/3] Jack compiler   (Jack -> VM intermediate code)
[2/3] VM translator   (VM -> Hack assembly)
[3/3] Assembler       (Hack assembly -> 16-bit machine code)

Pipeline complete: Jack source compiled all the way to machine code.
    VM functions defined : 22
    VM functions called  : 17  (all resolved)
    Machine-code words   : 5073  (all valid 16-bit binary)
    Output binary        : build/complete_program.hack
```

The demo program ([`examples/complete_program/`](examples/complete_program/))
is **self-contained**: it ships with a minimal runtime (`Sys`, `Memory`,
`Math`, `Array`) written in Jack and compiled by this project's own compiler, so
the stack is self-hosting for the language features it uses and the binary links
with no external dependencies.

### Running a single stage

**Compile Jack source to VM code:**
```bash
python jack_compiler/JackCompiler.py examples/jack_programs
# → writes Main.vm, Conv.vm into an adjacent out/ directory
```

**Translate VM code to Hack assembly:**
```bash
python vm_translator/main.py examples/vm_programs
# → writes vm_programs.asm (with VM bootstrap) next to the inputs
```

**Assemble Hack assembly to machine code:**
```bash
python assembler/assembler.py examples/assembly_programs/matrix_mult.asm
# → writes matrix_mult.hack (16-bit binary words)
```

The resulting `.hack` machine code is what the gate-level CPU in
[`hardware/`](hardware/) executes.

---

## Running the Tests

The test suite drives each backend stage as a black box and asserts on the
artifact it produces:

```bash
python -m unittest discover -s tests   # standard library
pytest                                 # if installed
```

---

## Repository Layout

```
.
├── README.md
├── pipeline.py                  # one-command Jack → VM → ASM → machine code driver
├── docs/
│   ├── architecture.md          # frontend / middle-end / backend, runtime & memory model
│   ├── compiler_pipeline.md     # pass-by-pass walk-through
│   └── design_decisions.md      # rationale behind the engineering choices
├── hardware/
│   ├── alu/                     # ALU + multiply path
│   ├── arithmetic/              # multipliers and adders
│   ├── memory/                  # RAM hierarchy
│   └── sequential/              # bit, register, counter
├── assembler/                   # Hack assembly → machine code
├── vm_translator/               # stack VM → Hack assembly
├── jack_compiler/               # Jack → VM code
├── examples/
│   ├── complete_program/        # self-contained Jack app + runtime (full pipeline demo)
│   ├── jack_programs/            # object-oriented Jack source (frontend showcase)
│   ├── vm_programs/              # stack-based VM source
│   └── assembly_programs/        # Hack assembly source
├── tests/                       # per-stage + full-stack tests
├── assets/                      # diagrams
└── .github/workflows/ci.yml     # CI: runs tests + full pipeline build on push
```

---

## Background

The instruction set, VM specification, and Jack language follow the
**Nand2Tetris** platform, which defines a clean, fully specified target for an
end-to-end stack. All compiler stages and hardware components here are original
implementations of that specification.
