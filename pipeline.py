#!/usr/bin/env python3
"""Drive the full compiler toolchain end to end: Jack -> VM -> ASM -> machine code.

Usage:
    python pipeline.py <jack_program_dir> [--build-dir DIR]

Given a directory of .jack source files (an application plus the runtime it
needs), this:

  1. compiles every class to VM code      (jack_compiler/)
  2. translates the VM code to assembly    (vm_translator/)
  3. assembles the assembly to machine code (assembler/)
  4. verifies the program is fully linked   (every called VM function is defined)
     and that every emitted machine-code word is a valid 16-bit binary instruction.

Each stage runs as a subprocess, exactly as a user would invoke it, so the three
tools stay decoupled (they even share module names like `parser.py`). The final
`.hack` binary is written to the build directory.
"""

import argparse
import glob
import os
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
PYTHON = sys.executable


def run_stage(title, argv):
    # Echo a readable command line: "python <tool> <args...>" with repo-relative paths.
    shown = ["python"] + [
        os.path.relpath(a, REPO) if os.path.isabs(a) and a.startswith(REPO) else a
        for a in argv[1:]
    ]
    print(f"  $ {' '.join(shown)}")
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode != 0:
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        sys.exit(f"[FAIL] {title} exited with code {result.returncode}")


def collect_symbols(vm_dir):
    """Return (defined functions, called functions, unresolved calls)."""
    defined = set()
    called = {}  # name -> source file where first called
    for vm in sorted(glob.glob(os.path.join(vm_dir, "*.vm"))):
        with open(vm) as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2 and parts[0] == "function":
                    defined.add(parts[1])
                elif len(parts) >= 2 and parts[0] == "call":
                    called.setdefault(parts[1], os.path.basename(vm))
    missing = {fn: src for fn, src in called.items() if fn not in defined}
    return defined, set(called), missing


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("program", help="directory of .jack files (app + runtime)")
    ap.add_argument("--build-dir", default=os.path.join(REPO, "build"),
                    help="output directory (default: ./build)")
    args = ap.parse_args()

    program = os.path.abspath(args.program)
    jack_files = sorted(glob.glob(os.path.join(program, "*.jack")))
    if not jack_files:
        sys.exit(f"no .jack files found in {program}")

    name = os.path.basename(program.rstrip("/\\"))
    build = os.path.abspath(args.build_dir)
    src = os.path.join(build, "src")
    out = os.path.join(build, "out")   # JackCompiler writes VM into <parent of input>/out

    if os.path.isdir(build):
        shutil.rmtree(build)
    os.makedirs(src)
    for jf in jack_files:
        shutil.copy(jf, src)

    print(f"Building '{name}' from {len(jack_files)} Jack source file(s)\n")

    print("[1/3] Jack compiler   (Jack -> VM intermediate code)")
    run_stage("jack compiler",
              [PYTHON, os.path.join(REPO, "jack_compiler", "JackCompiler.py"), src])

    print("[2/3] VM translator   (VM -> Hack assembly)")
    run_stage("vm translator",
              [PYTHON, os.path.join(REPO, "vm_translator", "main.py"), out])
    asm = os.path.join(out, "out.asm")

    print("[3/3] Assembler       (Hack assembly -> 16-bit machine code)")
    run_stage("assembler",
              [PYTHON, os.path.join(REPO, "assembler", "assembler.py"), asm])
    hack = os.path.join(out, "out.hack")

    # --- Linker-style verification: every called function must be defined. ---
    defined, called, missing = collect_symbols(out)
    if missing:
        print("\n[FAIL] program is not fully linked; unresolved calls:")
        for fn, srcfile in sorted(missing.items()):
            print(f"    {fn}   (first called in {srcfile})")
        sys.exit(1)

    # --- Verify the machine code is well-formed. ---
    with open(hack) as f:
        words = [w for w in f.read().splitlines() if w]
    malformed = [w for w in words if len(w) != 16 or (set(w) - {"0", "1"})]
    if malformed:
        sys.exit(f"[FAIL] {len(malformed)} malformed machine-code word(s)")

    final = os.path.join(build, f"{name}.hack")
    shutil.copy(hack, final)

    print("\nPipeline complete: Jack source compiled all the way to machine code.")
    print(f"    VM functions defined : {len(defined)}")
    print(f"    VM functions called  : {len(called)}  (all resolved)")
    print(f"    Machine-code words   : {len(words)}  (all valid 16-bit binary)")
    print(f"    Output binary        : {os.path.relpath(final, REPO)}")


if __name__ == "__main__":
    main()
