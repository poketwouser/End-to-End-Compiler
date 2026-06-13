load ROWXCOL.asm,
output-file ROWXCOL.out,
compare-to ROWXCOL.cmp,
output-list RAM[16]%D1.7.1;

repeat 3000 {
  ticktock;
}

output;
