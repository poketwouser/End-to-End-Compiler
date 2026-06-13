load SanityCheck.asm,
output-file SanityCheck.out,
compare-to SanityCheck.cmp,
output-list RAM[16]%D1.7.1;

// Run bootstrap + Sys.init
repeat 1000 {
  ticktock;
}

output;
