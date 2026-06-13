set sp 300,
set local 300,
set argument 400,
set RAM[400] 1234,
set RAM[401] 5678,

repeat 10 {
  vmstep;
}
