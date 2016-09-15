#!/usr/bin/python3

from parser import Parser

if __name__ == '__main__':
    p = Parser()
    bits = p.parse_instruction('addi $t1, $t2, 0x400')
    print(bits)
