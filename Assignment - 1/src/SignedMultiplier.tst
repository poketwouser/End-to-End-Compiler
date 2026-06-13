load SignedMultiplier.hdl,
output-file SignedMultiplier.out,
compare-to SignedMultiplier.cmp,
output-list a%D1.6.1 b%D1.6.1 out2%D1.10.1 out1%D1.10.1;

set a 0, set b 0, eval, output;
set a 1, set b 1, eval, output;
set a 2, set b 3, eval, output;
set a 7, set b 9, eval, output;
set a 15, set b 15, eval, output;
set a 255, set b 4, eval, output;
set a 123, set b 45, eval, output;
set a 32767, set b 2, eval, output;
set a %B1111111111111101, set b 5, eval, output;
set a 3, set b %B1111111111111011, eval, output;
set a %B1111111111111101, set b %B1111111111111011, eval, output;
set a %B1111111111111111, set b 1, eval, output;
set a 1, set b %B1111111111111111, eval, output;
set a %B1111111111111111, set b %B1111111111111111, eval, output;
set a 0, set b 32767, eval, output;
set a 32767, set b 0, eval, output;
set a 1, set b 32767, eval, output;
set a %B1000000000000000, set b 1, eval, output;
