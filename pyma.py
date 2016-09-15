#!/usr/bin/python3

from parser import Parser

def hexstr(bits):
    h = int(bits, 2)
    return '{0:08x}'.format(h)

if __name__ == '__main__':
    p = Parser()
    h = ''
    h += hexstr(p.parse_instruction('addi $t1, $t2, 0x400'))
    h += hexstr(p.parse_instruction('sll $t4, $t8, 0x4'))
    h += hexstr(p.parse_instruction('jr $t2'))
    print(h)
