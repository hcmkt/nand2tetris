import sys
import parser
import code
import symbol_table

args = sys.argv
file = args[1]

s = symbol_table.SymbolTable()
address = 0
with parser.Parser(file) as p:
    while p.advance():
        cmd_type = p.command_type()
        if cmd_type == 'L_COMMAND':
            symbol = p.symbol()
            if s.contains(symbol):
                raise Exception('Duplicate symbol')
            s.add_entry(symbol, address)
        else:
            address += 1

c = code.Code()
f = open(file.split('.')[0]+'.hack', 'w')
address = 16
with parser.Parser(file) as p:
    while p.advance():
        cmd_type = p.command_type()
        if cmd_type in ['A_COMMAND', 'C_COMMAND']:
            if cmd_type == 'A_COMMAND':
                symbol = p.symbol()
                if symbol.isdecimal():
                    addr = int(symbol)
                else:
                    if s.contains(symbol):
                        addr = s.get_address(symbol)
                    else:
                        s.add_entry(symbol, address)
                        addr = address
                        address += 1
                binary = '{:016b}'.format(addr)
            elif cmd_type == 'C_COMMAND':
                binary = '111' + c.comp(p.comp()) + c.dest(p.dest()) + c.jump(p.jump())
            f.write(binary + '\n')
f.close()
