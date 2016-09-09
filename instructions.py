#!/usr/bin/env python
import re

patterns = {
            'instruction':  re.compile(r'^[ \t]*(?P<instruction>.*?)[ \t]'),
            'comma':        re.compile(r'\s*,\s*'),
            'rd':           re.compile(r'(?P<rd>\$.+)'),
            'rs':           re.compile(r'(?P<rs>\$.+)'),
            'rt':           re.compile(r'(?P<rt>\$.+)'),
            'shamt':        re.compile(r'(?P<shamt>\d+)'),
            'i':            re.compile(r'(?P<i>\-?\d+)'),
            'i(rs)':        re.compile(r'(?P<i>\-?\d+)\((?P<rs>\$.+)\)'),
            'address':      re.compile(r'(?P<address>\d+)'),
           }

registers = {
            'zero': 0,
            'at':   1,
            'v0':   2,
            'v1':   3
            'a0':   4,
            'a1':   5,
            'a2':   6,
            'a3':   7,
            't0':   8,
            't1':   9,
            't2':   10,
            't3':   11,
            't4':   12,
            't5':   13,
            't6':   14,
            't7':   15,
            's0':   16,
            's1':   17,
            's2':   18,
            's3':   19,
            's4':   20,
            's5':   21,
            's6':   22,
            's7':   23,
            't8':   24,
            't9':   25,
            'k0':   26,
            'k1':   27,
            'gp':   28,
            'sp':   29,
            'fp':   30,
            'ra':   31,
            }

# function codes for R-Type instructions
# format:
# function code, syntax
r_types = {
            'sll':   (0x00, ('rd', 'rt', 'shamt')),
            'srl':   (0x02, ('rd', 'rt', 'shamt')),
            'sra':   (0x03, ('rd', 'rt', 'shamt')),
            'sllv':  (0x04, ('rd', 'rt', 'rs')),
            'srlv':  (0x06, ('rd', 'rt', 'rs')),
            'srav':  (0x07, ('rd', 'rt', 'rs')),
            'jr':    (0x08, ('rs')),
            'mfhi':  (0x10, ('rd')),
            'mflo':  (0x12, ('rd')),
            'mult':  (0x18, ('rs', 'rt')),
            'multu': (0x19, ('rs', 'rt')),
            'div':   (0x1A, ('rs', 'rt')),
            'divu':  (0x1B, ('rs', 'rt')),
            'add':   (0x20, ('rd', 'rs', 'rt')),
            'addu':  (0x21, ('rd', 'rs', 'rt')),
            'sub':   (0x22, ('rd', 'rs', 'rt')),
            'subu':  (0x23, ('rd', 'rs', 'rt')),
            'and':   (0x24, ('rd', 'rs', 'rt')),
            'or':    (0x25, ('rd', 'rs', 'rt')),
            'xor':   (0x26, ('rd', 'rs', 'rt')),
            'nor':   (0x27, ('rd', 'rs', 'rt')),
            'slt':   (0x2A, ('rd', 'rs', 'rt')),
            'sltu':  (0x2B, ('rd', 'rs', 'rt')),
          }

# opcodes for I-Type instructions
# format:
# opcode, rt replacement, syntax
i_types = {
            'beq':   (0x04, None, ('rt', 'rs', 'i')),
            'bne':   (0x05, None, ('rt', 'rs', 'i')),
            'addi':  (0x08, None, ('rt', 'rs', 'i')),
            'addiu': (0x09, None, ('rt', 'rs', 'i')),
            'andi':  (0x0C, None, ('rt', 'rs', 'i')),
            'lbu':   (0x24, None, ('rt', 'i(rs)')),
            'lhu':   (0x25, None, ('rt', 'i(rs)')),
            'lui':   (0x0F, None, ('rt', 'i')),
            'lw':    (0x23, None, ('rt', 'i(rs)')),
            'ori':   (0x0D, None, ('rt', 'rs', 'i')),
            'sb':    (0x28, None, ('rt', 'i(rs)'),
            'sh':    (0x29, None, ('rt', 'i(rs)'),
            'slti':  (0x0A, None, ('rt', 'rs', 'i')),
            'sltiu': (0x0B, None, ('rt', 'rs', 'i')),
            'sw':    (0x2B, None, ('rt', 'i(rs)')),
          }

# opcodes for J-Type instructions
j_types = {'j':     0x02,
           'jal':   0x03,
          }
