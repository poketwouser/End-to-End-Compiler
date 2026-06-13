"""End-to-end smoke tests for the compiler toolchain.

Each test drives one backend stage as a black box: it shells out to the
stage's entry point exactly as a user would, then asserts on the artifact
that stage is contracted to produce. Run from the repository root with:

    python -m unittest discover -s tests
    # or, if pytest is installed:
    pytest
"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(REPO_ROOT, "examples")
PYTHON = sys.executable


def run(entry_point, arg, cwd):
    """Invoke a stage entry point and fail loudly on a non-zero exit."""
    result = subprocess.run(
        [PYTHON, entry_point, arg],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(
            f"{entry_point} exited {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class TestAssembler(unittest.TestCase):
    """Hack assembly -> 16-bit machine code."""

    def test_emits_binary_machine_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            asm = os.path.join(tmp, "matrix_mult.asm")
            shutil.copy(
                os.path.join(EXAMPLES, "assembly_programs", "matrix_mult.asm"), asm
            )
            run(os.path.join(REPO_ROOT, "assembler", "assembler.py"), asm,
                cwd=os.path.join(REPO_ROOT, "assembler"))

            hack = os.path.join(tmp, "matrix_mult.hack")
            self.assertTrue(os.path.exists(hack), "no .hack file produced")
            with open(hack) as f:
                lines = [ln for ln in f.read().splitlines() if ln]
            self.assertGreater(len(lines), 0)
            for ln in lines:
                self.assertEqual(len(ln), 16, f"not a 16-bit word: {ln!r}")
                self.assertTrue(set(ln) <= {"0", "1"}, f"non-binary: {ln!r}")


class TestVMTranslator(unittest.TestCase):
    """Stack-based VM -> Hack assembly."""

    def test_emits_assembly_with_bootstrap(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("Main.vm", "Sys.vm"):
                shutil.copy(os.path.join(EXAMPLES, "vm_programs", name),
                            os.path.join(tmp, name))
            run(os.path.join(REPO_ROOT, "vm_translator", "main.py"), tmp,
                cwd=os.path.join(REPO_ROOT, "vm_translator"))

            asm = os.path.join(tmp, os.path.basename(tmp) + ".asm")
            self.assertTrue(os.path.exists(asm), "no .asm file produced")
            with open(asm) as f:
                text = f.read()
            # Directory translation must emit the VM bootstrap (SP=256; call Sys.init).
            self.assertIn("@256", text)
            self.assertIn("Sys.init", text)


class TestJackCompiler(unittest.TestCase):
    """Jack (object-oriented source) -> VM code."""

    def test_emits_vm_for_each_class(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "src")
            shutil.copytree(os.path.join(EXAMPLES, "jack_programs"), src)
            run(os.path.join(REPO_ROOT, "jack_compiler", "JackCompiler.py"), src,
                cwd=os.path.join(REPO_ROOT, "jack_compiler"))

            out = os.path.join(tmp, "out")
            self.assertTrue(os.path.isdir(out), "no out/ directory produced")
            main_vm = os.path.join(out, "Main.vm")
            self.assertTrue(os.path.exists(main_vm), "Main.vm not generated")
            # The entry point compiles to a VM function declaration.
            with open(main_vm) as f:
                self.assertIn("function Main.main", f.read())


if __name__ == "__main__":
    unittest.main(verbosity=2)
