# Hack VM Translator

## Requirements

- Python 3

## How to Execute

The translator can process either a single `.vm` file or an entire directory containing multiple `.vm` files.

### 1. Translate a Single File

To translate a single VM file, provide the path to the file as an argument:

```bash
python src/main.py tests/BasicTest/BasicTest.vm
```

This will generate a `BasicTest.asm` file in the same directory.

### 2. Translate a Directory

To translate an entire directory (for multi-file programs like Fibonacci), provide the path to the folder:

```bash
python src/main.py tests/FibonacciElement/
```

This will generate a single `.asm` file named after the folder (e.g., `FibonacciElement.asm`) and will automatically include the **Bootstrap Code** (initializing `SP=256` and calling `Sys.init`).

## Testing and Validation

Once you have generated the `.asm` file, you can verify it using the provided test scripts in the Nand2Tetris **CPU Emulator**:

1. Open the **Nand2Tetris CPU Emulator**.
2. Load the `.tst` file from the corresponding test folder (e.g., `tests/BasicTest/BasicTest.tst`).
3. Click the **Fast Forward** button.
4. The emulator will compare the output against the `.cmp` file and display "Comparison ended successfully" if the logic is correct.

## Project Structure

- `src/translator.py`: The main entry point.
- `src/parser.py`: Parses VM commands from the input files.
- `src/code_writer.py`: Generates Hack Assembly code for each VM command.
- `tests/`: Contains the test suites (BasicTest, FibonacciElement, etc.) with `.vm`, `.tst`, and `.cmp` files.
