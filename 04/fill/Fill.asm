// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

@8192
D = A 
@pix
M = D           // Get pixel limit

@SCREEN         // Get screen base address
D = A 
@screenBase
M = D

( LOOP )
    
    @KBD            // Get keyboard state
    D = M 

    @WIPE           // Wipe screen on no press
    D; JEQ

    @PAINT          // Paint on keypress
    D; JGT

( WIPE )

    @8192
    D = A 

    @pix
    M = D           // Reset pixel counter

    @screenBase
    D = M

    @n 
    A = D + M       // Set RAM address to screen base + n
    M = 0

    @n 
    D = M 

    @LOOP
    D; JEQ          // If n is zero, back to loop

    @n 
    M = M - 1       // Else, decrease n

    @LOOP
    0; JMP          // Back to Loop

( PAINT )

    @pix            
    D = M

    @LOOP
    D; JLE          // Return if we drew all pixels
    
    @pix
    M = D - 1

    @n 
    D = M 

    @screenBase
    A = M + D       // Set address to screen base + n
    M = -1          // Set screen to black

    @n 
    M = D + 1       // Increment n by 1

    @LOOP
    0; JMP          // Back to loop
