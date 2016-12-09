# pyma
A reduced-instruction-set MIPS assembler.
Currently handles R-type and I-type instructions which do not
involve labels. 

Usage:
./pyma prog.asm


Where prog.asm is a file containing one MIPS instruction per
line. Make sure that the program has no .data or .text sections.
Support for these will be implemented eventually.
