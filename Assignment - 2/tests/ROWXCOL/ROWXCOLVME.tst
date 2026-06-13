// VM Emulator test for ROWXCOL.dot
// row = [1, 2, 3] at RAM[100], col = [4, 5, 6] at RAM[200]
// Expected result on stack top: 32

set RAM[100] 1,
set RAM[101] 2,
set RAM[102] 3,

set RAM[200] 4,
set RAM[201] 5,
set RAM[202] 6,

// SP=270, LCL=270, ARG=260
set RAM[0] 270,
set RAM[1] 270,
set RAM[2] 260,

// arguments: row_ptr, col_ptr, length, col_stride
set RAM[260] 100,
set RAM[261] 200,
set RAM[262] 3,
set RAM[263] 1,

// fake frame
set RAM[264] 999,
set RAM[265] 0,
set RAM[266] 0,
set RAM[267] 0,
set RAM[268] 0,

repeat 150 {
  vmstep;
}
