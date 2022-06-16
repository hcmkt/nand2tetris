import glob
import os
import sys
import parser
import code_writer

args = sys.argv
arg = args[1]
if os.path.isfile(arg):
    files = [arg]
    file = arg.split('.')[0]
else:
    files = glob.glob(os.path.join(arg, '**', '*.vm'), recursive=True)
    file = arg[0:-1] if arg[-1] == '/' else arg
c = code_writer.CodeWriter(file + '.asm')
for file in files:
    c.set_file_name(os.path.basename(file).split('.')[0])
    with parser.Parser(file) as p:
        while p.advance():
            cmd_type = p.command_type()
            if cmd_type == 'C_ARITHMETIC':
                c.write_arithmetic(p.arg1())
            elif cmd_type in ['C_PUSH', 'C_POP']:
                c.write_push_pop(cmd_type, p.arg1(), p.arg2())
c.close()
