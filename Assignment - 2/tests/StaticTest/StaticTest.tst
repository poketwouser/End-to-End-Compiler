load StaticTest.asm,
output-file StaticTest.out,
compare-to StaticTest.cmp,
output-list RAM[0]%D1.7.1 RAM[256]%D1.7.1;

set RAM[0] 256,

repeat 200 {
  ticktock;
}

output;
