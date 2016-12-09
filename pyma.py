#!/usr/bin/python3

from parser import Parser

def hexstr(bits):
    h = int(bits, 2)
    return '{0:08x}'.format(h)

if __name__ == '__main__':
    f = open("prog2.asm")
    p = Parser()
    h = ''
    for line in f:
        h += hexstr(p.parse_instruction(line)) + '\n'
    print(h)
