// push constant 10
@10
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop local 0
@0
D=A
@LCL
MD=D+M
@SP
AM=M-1
D=M
@LCL
A=M
M=D
@0
D=A
@LCL
M=M-D
// push constant 21
@21
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 22
@22
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop argument 2
@2
D=A
@ARG
MD=D+M
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@2
D=A
@ARG
M=M-D
// pop argument 1
@1
D=A
@ARG
MD=D+M
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@1
D=A
@ARG
M=M-D
// push constant 36
@36
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop this 6
@6
D=A
@THIS
MD=D+M
@SP
AM=M-1
D=M
@THIS
A=M
M=D
@6
D=A
@THIS
M=M-D
// push constant 42
@42
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 45
@45
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop that 5
@5
D=A
@THAT
MD=D+M
@SP
AM=M-1
D=M
@THAT
A=M
M=D
@5
D=A
@THAT
M=M-D
// pop that 2
@2
D=A
@THAT
MD=D+M
@SP
AM=M-1
D=M
@THAT
A=M
M=D
@2
D=A
@THAT
M=M-D
// push constant 510
@510
D=A
@SP
A=M
M=D
@SP
AM=M+1
// pop temp 6
@6
D=A
@R5
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
// push local 0
@0
D=A
@LCL
A=D+M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// push that 5
@5
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// push this 6
@6
D=A
@THIS
A=D+M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// push this 6
@6
D=A
@THIS
A=D+M
D=M
@SP
A=M
M=D
@SP
AM=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// push temp 6
@6
D=A
@R5
A=D+A
D=M
@SP
A=M
M=D
@SP
AM=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=M+D
