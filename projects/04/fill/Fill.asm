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

// initialize termination case for drawing

@8192
D=A
@R0
M=D

(START)
    @KBD
    D=M
    @FILL
    D;JGT

    // start loop to clear screen
    @i
    M=0
    (CLEARLOOP)
        // check if termination case
        @R0
        D=M
        @i
        D = M - D
        @START
        D;JEQ

        // main work of loop
        @i
        D = M
        @SCREEN
        A = A + D
        M=0
        @i
        M = M + 1
        @CLEARLOOP
        0;JMP

(FILL)
    // start loop to draw on screen
    @i
    M=0
    (DRAWLOOP)
        // check if termination case
        @R0
        D=M
        @i
        D = M - D
        @START
        D;JEQ

        // main work of loop
        @i
        D = M
        @SCREEN
        A = A + D
        M=-1
        @i
        M = M + 1
        @DRAWLOOP
        0;JMP

@START
0;JMP