// Matrix Multiplication c = a * b
// Assuming a is at 100, b is at 110, c is at 120
// We need to do c[i][j] = sum(a[i][k] * b[k][j])

// Matrix Initialization
// A:
// 1 2 3
// 4 5 6
// 7 8 9
@100
M=1
@101
M=2
@102
M=3
@103
M=4
@104
M=5
@105
M=6
@106
M=7
@107
M=8
@108
M=9

// B:
// 1 0 0
// 0 1 0
// 0 0 1
@110
M=1
@111
M=0
@112
M=0
@113
M=0
@114
M=1
@115
M=0
@116
M=0
@117
M=0
@118
M=1

// Algorithm:
// i = 0
(LOOP_I_INIT)
@i
M=0

(LOOP_I_START)
@i
D=M
@3
D=D-A
@END
D;JGE  // if i>=3 goto END

// j = 0
(LOOP_J_INIT)
@j
M=0

(LOOP_J_START)
@j
D=M
@3
D=D-A
@LOOP_J_END
D;JGE  // if j>=3 goto LOOP_J_END

// sum = 0
@sum
M=0

// k = 0
(LOOP_K_INIT)
@k
M=0

(LOOP_K_START)
@k
D=M
@3
D=D-A
@LOOP_K_END
D;JGE  // if k>=3 goto LOOP_K_END

// a_val = A[i*3 + k] = RAM[100 + i*3 + k]
// compute i*3:
@i
D=M
@i3
M=D
@i
D=M
@i3
M=M+D
@i
D=M
@i3
M=M+D // i3 = i*3

@100
D=A
@i3
D=D+M
@k
D=D+M // D = 100 + i*3 + k = a_addr
@a_addr
M=D   // save a_addr

// a_val = RAM[a_addr]
@a_addr
A=M
D=M
@a_val
M=D

// compute k*3:
@k
D=M
@k3
M=D
@k
D=M
@k3
M=M+D
@k
D=M
@k3
M=M+D // k3 = k*3

// b_addr = 110 + k*3 + j
@110
D=A
@k3
D=D+M
@j
D=D+M
@b_addr
M=D

// b_val = RAM[b_addr]
@b_addr
A=M
D=M
@b_val
M=D

// multiply a_val * b_val via repeated addition
// prod = 0
@prod
M=0
// p = 0
@p
M=0

(MULTIPLY_LOOP)
@p
D=M
@b_val
D=D-M
@MULTIPLY_END
D;JGE // if p >= b_val goto MULTIPLY_END

@a_val
D=M
@prod
M=M+D // prod += a_val

@p
M=M+1
@MULTIPLY_LOOP
0;JMP

(MULTIPLY_END)

// sum = sum + prod
@prod
D=M
@sum
M=M+D

// k++
@k
M=M+1
@LOOP_K_START
0;JMP

(LOOP_K_END)

// C[i*3 + j] = sum
// A_addr was 100 + ... but we need 120 + i*3 + j
// We already have i3 as i*3 from the inner loop
@120
D=A
@i3
D=D+M
@j
D=D+M
@c_addr
M=D

@sum
D=M
@c_addr
A=M
M=D

// j++
@j
M=M+1
@LOOP_J_START
0;JMP

(LOOP_J_END)

// i++
@i
M=M+1
@LOOP_I_START
0;JMP

(END)
@END
0;JMP
