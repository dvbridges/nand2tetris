// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// Take one of the values for the number of loops: n
// Take one of the values for adding to the sum: val
// Create a sum variable for the sum of all vals: sum


@R0
D = M
@n
M = D           // n = R0
@R1
D = M 
@val
M = D           // val = R1
@sum
M = 0
@R2
M = 0           // Reset output value

( LOOP )
    @sum
    D = M       // Put sum in data register
    @val
    D = D + M   // Add val to sum
    @sum
    M = D       // Set sum in memory     
    @n 
    D = M - 1   // Decrease n by 1
    M = D       // Set n in memory
    @STOP
    D; JEQ      // goto STOP if n == 0
    @LOOP
    0; JMP      // Restart Loop

( STOP )
    @sum
    D = M       // Get sum
    @R2
    M = D       // Set R2 to sum val

( END )
    @END
    0;JMP 
