// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

// set i=0
@i
M=0

// set product = 0
@product
M=0

(LOOP)
    // check if i-R1==0
    @i
    D=M
    @R1
    D=D-M
    @STOP
    D;JEQ

    // main work of loop
    // product = product + R0
    // i = i + 1
    @R0
    D=M
    @product
    M=M+D
    @i
    M=M+1
    @LOOP
    0;JMP

// STOP logic
(STOP)
    @product
    D=M
    @R2
    M=D

(END)
    @END
    0;JMP