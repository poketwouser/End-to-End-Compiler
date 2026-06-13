load SimpleAdd.asm,
output-file SimpleAdd.out,
compare-to SimpleAdd.cmp,
output-list RAM[0]%D1.7.1 RAM[256]%D1.7.1;

set RAM[0] 256,

repeat 60 {
  ticktock;
}

output;
