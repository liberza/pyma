#!/usr/bin/env python
import re
from exceptions import SyntaxException
from mappings import Mappings

# need to go through file once, noting all labels and their associated instruction number.
# if a label is on the same line as an instruction, use that instruction number
# otherwise, find the next instruction and use that number.

class Parser():
    def get_register(self, r):
    '''
    Returns the register number associated with r.
    If r is the string representation of a register number, it 
    gets returned as an int.
    '''
        if r in Mappings.registers:
            return Mappings.registers[r]
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
    '''
    Parses a particular line, returning the bit pattern for an instruction if possible.
    A SyntaxException will be raised on error.
    If no instruction was found on the line, this will return False.
    '''
        r_groups = ['rt', 'rs', 'rd', 'shamt']
        i_groups = ['rt', 'rs', 'i']
        j_groups = ['address']
        # allow for labels on the same line as an instruction.
        pattern = Mappings.patterns['label'] + Mappings.patterns['instruction']
        m = re.search(pattern, line)
        i = Mappings.instructions.get(m.group('instruction'))
        j = 1
        if i is not None:
            for arg in i['syntax']:
                pattern += Mappings.patterns[p]
                if j != len(i['syntax']):
                    pattern += Mappings.patterns['comma']
                j += 1
            pattern += Mappings.patterns['eol']
                
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
    '''
    Returns the bit sequence for the r-type instruction as a string.
    '''
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
    '''
    Returns the bit sequence for the i-type instruction as a string.
    '''
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
    '''
    Returns the bit sequence for the j-type instruction as a string.
    '''
        address = str_to_val(address, 26)
        bits = ''
        bits += '{0:6b}'.format(op)
        bits += '{0:26b}'.format(address)
        return bits
