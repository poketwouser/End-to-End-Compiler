load FibonacciElement.asm,
output-file FibonacciElement.out,
compare-to FibonacciElement.cmp,
output-list RAM[0]%D1.7.1 RAM[261]%D1.7.1;

repeat 6000 {
  ticktock;
}

output;
