# Complete Program — full top-to-bottom demo

This directory holds a **self-contained** Jack program that the toolchain
compiles all the way from source to executable Hack machine code, with every
called function resolved.

It is the program driven by [`../../pipeline.py`](../../pipeline.py):

```bash
python pipeline.py examples/complete_program
```

## What's here

| File          | Role                                                              |
|---------------|-------------------------------------------------------------------|
| `Main.jack`   | Application entry point.                                           |
| `Stats.jack`  | An object computing sum / mean / max over an array.               |
| `Sys.jack`    | Bootstrap: brings up the runtime, then calls `Main.main`.         |
| `Memory.jack` | Heap allocator + `peek`/`poke` (the runtime's memory manager).    |
| `Math.jack`   | `multiply` / `divide` — the routines `*` and `/` lower to.        |
| `Array.jack`  | Heap-backed arrays.                                               |

`Sys`, `Memory`, `Math`, and `Array` form a **minimal runtime written in Jack
and compiled by this project's own compiler** — the stack is self-hosting for
the language features the demo uses. (The full Nand2Tetris OS adds graphics,
strings, and keyboard I/O; those are intentionally out of scope here so the demo
stays small and fully verifiable.)

## What it computes

The program builds the array of perfect squares `1, 4, 9, …, 64` and writes
three results into a fixed RAM inspection block:

| Address    | Value | Meaning            |
|------------|-------|--------------------|
| `RAM[8000]`| 204   | sum of the array   |
| `RAM[8001]`| 25    | integer mean (204/8)|
| `RAM[8002]`| 64    | maximum element    |

There is no screen output: results are published to memory so the program needs
no graphics runtime, and the pipeline can verify the build structurally (all
calls resolved, all machine-code words valid 16-bit binary). To watch it
*execute*, load the generated `build/complete_program.hack` into a Hack CPU
emulator and inspect those RAM addresses.
