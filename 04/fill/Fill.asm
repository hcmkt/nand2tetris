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

(Loop)
@i
M=1
@SCREEN
D=A
@Screen
M=D
@KBD
D=M
@White
D;JEQ
@color
M=-1
@SLoop
0;JMP
(White)
@color
M=0
(SLoop)
@i
D=M
@8192
D=D-A
@SEnd
D;JGT
@color
D=M
@Screen
A=M
M=D
@i
M=M+1
@Screen
M=M+1
@SLoop
0;JMP
(SEnd)
@Loop
0;JMP
