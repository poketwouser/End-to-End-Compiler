load ALU.hdl,
output-file ALU-Mul.out,
compare-to ALU-Mul.cmp,
output-list x%D1.6.1 y%D1.6.1 zx%B1.1.1 nx%B1.1.1 zy%B1.1.1 ny%B1.1.1 f%B1.1.1 no%B1.1.1 out%D1.6.1 zr%B1.1.1 ng%B1.1.1;

set x 13, set y 27, set zx 1, set nx 0, set zy 1, set ny 0, set f 1, set no 0, eval, output;

set x 13, set y 27, set zx 1, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;

set x 13, set y 27, set zx 1, set nx 1, set zy 1, set ny 0, set f 1, set no 0, eval, output;

set x 13, set y 27, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 0, eval, output;

set x 13, set y 27, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 0, eval, output;

set x 13, set y 27, set zx 0, set nx 0, set zy 1, set ny 1, set f 0, set no 1, eval, output;

set x 13, set y 27, set zx 1, set nx 1, set zy 0, set ny 0, set f 0, set no 1, eval, output;

set x 13, set y 27, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 1, eval, output;

set x 13, set y 27, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;

set x 13, set y 27, set zx 0, set nx 1, set zy 1, set ny 1, set f 1, set no 1, eval, output;

set x 13, set y 27, set zx 1, set nx 1, set zy 0, set ny 1, set f 1, set no 1, eval, output;

set x 13, set y 27, set zx 0, set nx 0, set zy 1, set ny 1, set f 1, set no 0, eval, output;

set x 13, set y 27, set zx 1, set nx 1, set zy 0, set ny 0, set f 1, set no 0, eval, output;

set x 13, set y 27, set zx 0, set nx 0, set zy 0, set ny 0, set f 1, set no 0, eval, output;

set x 13, set y 27, set zx 0, set nx 1, set zy 0, set ny 0, set f 1, set no 1, eval, output;

set x 13, set y 27, set zx 0, set nx 0, set zy 0, set ny 1, set f 1, set no 1, eval, output;

set x 13, set y 27, set zx 0, set nx 0, set zy 0, set ny 0, set f 0, set no 0, eval, output;

set x 13, set y 27, set zx 0, set nx 1, set zy 0, set ny 1, set f 0, set no 1, eval, output;

set x 3, set y 5, set zx 1, set nx 1, set zy 1, set ny 1, set f 0, set no 0, eval, output;
set x 7, set y 9, set zx 1, set nx 1, set zy 1, set ny 1, set f 0, set no 0, eval, output;

set x %B1111111111111101, set y 5, set zx 1, set nx 1, set zy 1, set ny 1, set f 0, set no 0, eval, output;

set x 3, set y %B1111111111111011, set zx 1, set nx 1, set zy 1, set ny 1, set f 0, set no 0, eval, output;

set x %B1111111111111101, set y %B1111111111111011, set zx 1, set nx 1, set zy 1, set ny 1, set f 0, set no 0, eval, output;

set x 0, set y 0, set zx 1, set nx 1, set zy 1, set ny 1, set f 0, set no 0, eval, output;
