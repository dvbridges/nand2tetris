// push constant 17
@17
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 17
@17
D=A
@sp
A=M
M=D
@sp
M=M+1
// eq
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JEQ
@sp
A=M
M=D
// push constant 17
@17
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 16
@16
D=A
@sp
A=M
M=D
@sp
M=M+1
// eq
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JEQ
@sp
A=M
M=D
// push constant 16
@16
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 17
@17
D=A
@sp
A=M
M=D
@sp
M=M+1
// eq
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JEQ
@sp
A=M
M=D
// push constant 892
@892
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 891
@891
D=A
@sp
A=M
M=D
@sp
M=M+1
// lt
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JLT
@sp
A=M
M=D
// push constant 891
@891
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 892
@892
D=A
@sp
A=M
M=D
@sp
M=M+1
// lt
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JLT
@sp
A=M
M=D
// push constant 891
@891
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 891
@891
D=A
@sp
A=M
M=D
@sp
M=M+1
// lt
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JLT
@sp
A=M
M=D
// push constant 32767
@32767
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 32766
@32766
D=A
@sp
A=M
M=D
@sp
M=M+1
// gt
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JGT
@sp
A=M
M=D
// push constant 32766
@32766
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 32767
@32767
D=A
@sp
A=M
M=D
@sp
M=M+1
// gt
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JGT
@sp
A=M
M=D
// push constant 32766
@32766
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 32766
@32766
D=A
@sp
A=M
M=D
@sp
M=M+1
// gt
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D;JGT
@sp
A=M
M=D
// push constant 57
@57
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 31
@31
D=A
@sp
A=M
M=D
@sp
M=M+1
// push constant 53
@53
D=A
@sp
A=M
M=D
@sp
M=M+1
// add
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D=D+M
@sp
A=M
M=D
// push constant 112
@112
D=A
@sp
A=M
M=D
@sp
M=M+1
// sub
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D+D-M
@sp
A=M
M=D
// neg
@sp
M=M-1
A=M
D=-D
@sp
A=M
M=D
// and
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D=D&M
@sp
A=M
M=D
// push constant 82
@82
D=A
@sp
A=M
M=D
@sp
M=M+1
// or
@sp
M=M-1
A=M
D=M
@sp
M=M-1
A=M
D=D|M
@sp
A=M
M=D
// not
@sp
M=M-1
A=M
D=!D
@sp
A=M
M=D
