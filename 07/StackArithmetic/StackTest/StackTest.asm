// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@26
D=D;JEQ
@SP
A=M-1
M=0
@30
0;JMP
@33
@SP
A=M-1
M=-1
@36
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
AM=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@57
D=D;JEQ
@SP
A=M-1
M=0
@61
0;JMP
@64
@SP
A=M-1
M=-1
@67
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
AM=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@88
D=D;JEQ
@SP
A=M-1
M=0
@92
0;JMP
@95
@SP
A=M-1
M=-1
@98
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@119
D=D;JLT
@SP
A=M-1
M=0
@123
0;JMP
@126
@SP
A=M-1
M=-1
@129
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
AM=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@150
D=D;JLT
@SP
A=M-1
M=0
@154
0;JMP
@157
@SP
A=M-1
M=-1
@160
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
AM=M+1
// lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@181
D=D;JLT
@SP
A=M-1
M=0
@185
0;JMP
@188
@SP
A=M-1
M=-1
@191
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@212
D=D;JGT
@SP
A=M-1
M=0
@216
0;JMP
@219
@SP
A=M-1
M=-1
@222
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
AM=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@243
D=D;JGT
@SP
A=M-1
M=0
@247
0;JMP
@250
@SP
A=M-1
M=-1
@253
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
AM=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@274
D=D;JGT
@SP
A=M-1
M=0
@278
0;JMP
@281
@SP
A=M-1
M=-1
@284
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
AM=M+1
// push constant 53
@53
D=A
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
// push constant 112
@112
D=A
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
// neg
@SP
A=M-1
M=-M
// and
@SP
AM=M-1
D=M
A=A-1
M=M&D
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
AM=M+1
// or
@SP
AM=M-1
D=M
A=A-1
M=M|D
// not
@SP
A=M-1
M=!M
