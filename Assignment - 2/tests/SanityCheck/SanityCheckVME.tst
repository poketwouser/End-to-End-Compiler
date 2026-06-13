// W is 2x3, X is 2x2 -> W_cols(3) != X_rows(2) -> FAIL
// Expected: static 0 (ERROR_LOC) = -1

// Arguments: W_rows, W_cols, X_rows, X_cols, B_rows, B_cols
set RAM[0] 270,
set RAM[1] 270,
set RAM[2] 259,

set RAM[259] 2,    // W_rows = 2
set RAM[260] 3,    // W_cols = 3
set RAM[261] 2,    // X_rows = 2  (MISMATCH: should be 3)
set RAM[262] 2,    // X_cols = 2
set RAM[263] 2,    // B_rows = 2
set RAM[264] 1,    // B_cols = 1

// Fake saved frame
set RAM[265] 999,
set RAM[266] 0,
set RAM[267] 0,
set RAM[268] 0,
set RAM[269] 0,

repeat 50 {
  vmstep;
}
