from symtable import Symbol
import sys
import parser
import code
import symol_table

args = sys.argv
file = args[1]
p = parser.Parser(file)
f = open('Prog.hack', 'w')
while p.advance():
    cmd_type = p.command_type()
    if cmd_type == 'A_COMMAND':
        binary = '{:016b}'.format(int(p.symbol()))
    else:
        c = code.Code()
        binary = '111' + c.comp(p.comp()) + c.dest(p.dest()) + c.jump(p.jump())
    f.write(binary + '\n')
f.close()
