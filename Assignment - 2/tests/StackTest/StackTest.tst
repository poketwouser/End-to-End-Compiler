load StackTest.asm,
output-file StackTest.out,
compare-to StackTest.cmp,
output-list RAM[0]%D1.7.1 RAM[256]%D1.7.1 RAM[257]%D1.7.1 RAM[258]%D1.7.1 RAM[259]%D1.7.1 RAM[260]%D1.7.1 RAM[261]%D1.7.1 RAM[262]%D1.7.1 RAM[263]%D1.7.1 RAM[264]%D1.7.1 RAM[265]%D1.7.1;

set RAM[0] 256,

repeat 1000 {
  ticktock;
}

output;
