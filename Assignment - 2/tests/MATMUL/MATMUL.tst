load MATMUL.asm,
output-file MATMUL.out,
compare-to MATMUL.cmp,
output-list RAM[400]%D1.7.1 RAM[401]%D1.7.1 RAM[402]%D1.7.1 RAM[403]%D1.7.1;

set RAM[100] 1,
set RAM[101] 2,
set RAM[102] 3,
set RAM[103] 4,

set RAM[200] 1,
set RAM[201] 0,
set RAM[202] 0,
set RAM[203] 1,

set RAM[300] 0,
set RAM[301] 0,

repeat 40000 {
  ticktock;
}

output;
