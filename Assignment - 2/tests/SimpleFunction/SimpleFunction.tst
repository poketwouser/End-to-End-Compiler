load SimpleFunction.asm,
output-file SimpleFunction.out,
compare-to SimpleFunction.cmp,
output-list RAM[0]%D1.7.1 RAM[1]%D1.7.1 RAM[2]%D1.7.1 RAM[3]%D1.7.1 RAM[4]%D1.7.1 RAM[400]%D1.7.1;

set RAM[0] 315,
set RAM[1] 315,
set RAM[2] 400,
set RAM[400] 1234,
set RAM[401] 5678,
set RAM[310] 999,
set RAM[311] 300,
set RAM[312] 400,
set RAM[313] 3000,
set RAM[314] 3010,

repeat 300 {
  ticktock;
}

output;
