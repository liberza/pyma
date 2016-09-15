#!/usr/bin/env python
import re

# need to go through file once, noting all labels and their associated instruction number.
# if a label is on the same line as an instruction, use that instruction number
# otherwise, find the next instruction and use that number.

class SyntaxException(Exception):
    pass

class Parser():
    patterns = {
        'instruction':  r'^(?:[\s]*.+:)*[\s]*(?P<instruction>[a-zA-Z0-9]+?)(?!:)[\s]',
        'comma':        r'[\s]*,[\s]*',
        'rd':           r'\$(?P<rd>[a-zA-Z0-9]+)',
        'rs':           r'\$(?P<rs>[a-zA-Z0-9]+)',
        'rt':           r'\$(?P<rt>[a-zA-Z0-9]+)',
        'shamt':        r'(?P<shamt>\d+)',
        'i':            r'(?P<i>\-?\d+)',
        'i(rs)':        r'(?P<i>\-?\d+)\((?P<rs>\$.+)\)',
        'address':      r'(?P<address>\d+)',
        'label':        r'^[\s]*(?P<label>.+:)',
        'eol':          r'[\s]*;?[\s]*(?:#.*)?$',
        }

    registers = {
        'zero': 0,
        'at':   1,
        'v0':   2,
        'v1':   3,
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

    instructions = {
        # r types
        'sll':   {'type':'r', 'func':0x00, 'op':0, 'syntax':('rd', 'rt', 'shamt')},
        'srl':   {'type':'r', 'func':0x02, 'op':0, 'syntax':('rd', 'rt', 'shamt')},
        'sra':   {'type':'r', 'func':0x03, 'op':0, 'syntax':('rd', 'rt', 'shamt')},
        'sllv':  {'type':'r', 'func':0x04, 'op':0, 'syntax':('rd', 'rt', 'rs')},
        'srlv':  {'type':'r', 'func':0x06, 'op':0, 'syntax':('rd', 'rt', 'rs')},
        'srav':  {'type':'r', 'func':0x07, 'op':0, 'syntax':('rd', 'rt', 'rs')},
        'jr':    {'type':'r', 'func':0x08, 'op':0, 'syntax':('rs')},
        'mfhi':  {'type':'r', 'func':0x10, 'op':0, 'syntax':('rd')},
        'mflo':  {'type':'r', 'func':0x12, 'op':0, 'syntax':('rd')},
        'mult':  {'type':'r', 'func':0x18, 'op':0, 'syntax':('rs', 'rt')},
        'multu': {'type':'r', 'func':0x19, 'op':0, 'syntax':('rs', 'rt')},
        'div':   {'type':'r', 'func':0x1A, 'op':0, 'syntax':('rs', 'rt')},
        'divu':  {'type':'r', 'func':0x1B, 'op':0, 'syntax':('rs', 'rt')},
        'add':   {'type':'r', 'func':0x20, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'addu':  {'type':'r', 'func':0x21, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'sub':   {'type':'r', 'func':0x22, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'subu':  {'type':'r', 'func':0x23, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'and':   {'type':'r', 'func':0x24, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'or':    {'type':'r', 'func':0x25, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'xor':   {'type':'r', 'func':0x26, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'nor':   {'type':'r', 'func':0x27, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'slt':   {'type':'r', 'func':0x2A, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'sltu':  {'type':'r', 'func':0x2B, 'op':0, 'syntax':('rd', 'rs', 'rt')},
        'mfc0':  {'type':'r', 'op':0x16, 'op':0, 'syntax':('rd', 'rs')},
        # i types
        'beq':   {'type':'i', 'op':0x04, 'syntax':('rt', 'rs', 'i')},
        'bne':   {'type':'i', 'op':0x05, 'syntax':('rt', 'rs', 'i')},
        'addi':  {'type':'i', 'op':0x08, 'syntax':('rt', 'rs', 'i')},
        'addiu': {'type':'i', 'op':0x09, 'syntax':('rt', 'rs', 'i')},
        'slti':  {'type':'i', 'op':0x0A, 'syntax':('rt', 'rs', 'i')},
        'sltiu': {'type':'i', 'op':0x0B, 'syntax':('rt', 'rs', 'i')},
        'andi':  {'type':'i', 'op':0x0C, 'syntax':('rt', 'rs', 'i')},
        'ori':   {'type':'i', 'op':0x0D, 'syntax':('rt', 'rs', 'i')},
        'lui':   {'type':'i', 'op':0x0F, 'syntax':('rt', 'i')},
        'lbu':   {'type':'i', 'op':0x24, 'syntax':('rt', 'i(rs)')},
        'lhu':   {'type':'i', 'op':0x25, 'syntax':('rt', 'i(rs)')},
        'lw':    {'type':'i', 'op':0x23, 'syntax':('rt', 'i(rs)')},
        'sb':    {'type':'i', 'op':0x28, 'syntax':('rt', 'i(rs)')},
        'sh':    {'type':'i', 'op':0x29, 'syntax':('rt', 'i(rs)')},
        'sw':    {'type':'i', 'op':0x2B, 'syntax':('rt', 'i(rs)')},
        # j types
        'j':     {'type':'j', 'op':0x02},
        'jal':   {'type':'j', 'op':0x03},
        }


    def get_register(self, r):
    '''
    Returns the register number associated with r.
    If r is the string representation of a register number, it 
    gets returned as an int.
    '''
        if r in self.registers:
            return self.registers[r]
        else if (int(r) >= 0) and (int(r) <= 31):
            return int(r)
        else:
            raise SyntaxException('Invalid register ' + r + ' on line ' + self.linenum)


    def str_to_val(self, valstr, n=32):
    '''
    Converts a string to an int, and optionally
    limits that int to less than 2^n.
    '''
        val = int(valstr)
        if (val < pow(2, n)):
            return val
        else:
            raise SyntaxException('Value ' + valstr + ' larger than ' + str(pow(2, n)))


    def parse_instruction(self, line):
        r_groups = ['rt', 'rs', 'rd', 'shamt']
        i_groups = ['rt', 'rs', 'i']
        j_groups = ['address']
        # allow for labels on the same line as an instruction.
        pattern = patterns['label'] + patterns['instruction']
        m = re.search(pattern, line)
        i = self.instructions.get(m.group('instruction'))
        j = 1
        if i is not None:
            for arg in i['syntax']:
                pattern += patterns[p]
                if j != len(i['syntax']):
                    pattern += patterns['comma']
                j += 1
            pattern += patterns['eol']
                
            m = re.search(pattern, line)
            a = {}
            for arg in i['syntax']:
                if arg == 'i(rs)':
                    # special case
                    try:
                        a['i'] = m.group['i']
                    except:
                        raise SyntaxException('Expected i on line ' + self.linenum)
                    try:
                        a['rs'] = m.group['rs']
                    except:
                        raise SyntaxException('Expected rs on line ' + self.linenum)
                else:
                    try:
                        a[arg] = m.group[arg]
                    except:
                        raise SyntaxException('Expected ' + arg + ' on line ' + self.linenum)


            # set unused values to 0,
            # then assemble bit sequence based on instruction type.
            if i['type'] == 'r':
                for arg in r_groups:
                    if arg not in a:
                        a[arg] = 0
                bits = assemble_rtype(i['func'], a['rs'], a['rt'], a['rd'], a['shamt'], i['op'])
            elif i['type'] == 'i':
                for arg in i_groups:
                    if arg not in a:
                        a[arg] = 0
                bits = assemble_itype(i['op'], a['rs'], a['rt'], a['i'])
            elif i['type'] == 'j':
                for arg in j_groups:
                    if arg not in a:
                        a[arg] = 0
                bits = assemble_jtype(i['op'], a['address'])
            else:
                raise SyntaxException('Unsupported instruction type.')
            return bits

        else:
            return False


    def assemble_rtype(self, func, rs, rt, rd, shamt, op):
        rs = get_register(rs)
        rt = get_register(rt)
        rd = get_register(rd)
        shamt = str_to_val(shamt, 5)
        bits = ''
        bits += '{0:6b}'.format(op)
        bits += '{0:5b}'.format(rs)
        bits += '{0:5b}'.format(rt)
        bits += '{0:5b}'.format(rd)
        bits += '{0:5b}'.format(shamt)
        bits += '{0:6b}'.format(func)
        return bits


    def assemble_itype(self, op, rt, rs, i):
        rt = get_register(rt)
        rs = get_register(rs)
        i = str_to_val(i, 16)
        bits = ''
        bits += '{0:6b}'.format(op)
        bits += '{0:5b}'.format(rs)
        bits += '{0:5b}'.format(rt)
        bits += '{0:16b}'.format(i)
        return bits


    def assemble_jtype(self, op, address):
        address = str_to_val(address, 26)
        bits = ''
        bits += '{0:6b}'.format(op)
        bits += '{0:26b}'.format(address)
        return bits
