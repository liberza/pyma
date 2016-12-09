#!/usr/bin/python3

from parser import Parser
import sys

def hexstr(bits):
    h = int(bits, 2)
    return '{0:08x}'.format(h)

# Parse a MIPS program
if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("Usage: ./pyma <program>")
        exit();
    f = open(sys.argv[1])
    p = Parser()
    h = ''
    for line in f:
        h += hexstr(p.parse_instruction(line)) + '\n'
    print(h)
