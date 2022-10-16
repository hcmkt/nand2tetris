from operator import truediv
import re

A_COMMAND = re.compile(r'@(?:\w|.)+')
C_COMMAND = re.compile(r'(?:(null|(?:A?M?D?))=)?(0|1|\-1|[AMD][\+\-]1|D[\+\-&\|][AM]|[AM]\-D|[!\-]?[AMD])(?:;(null|(?:J(?:GT|EQ|GE|LT|NE|LE|MP))))?')
L_COMMAND = re.compile(r'\((?:\w|.)+\)')

class Parser:
    def __init__(self, file):
        self.f = open(file, 'r')
        self.command = None

    def __enter__(self):
        return self
    
    def __exit__(self, ex_type, ex_value, trace):
        self.f.close()

    def advance(self):
        while True:
            str = self.f.readline()
            str = str.replace(' ', '')
            if str == '':
                return False
            else:
                str = str[0:str.find('//')]
                str = str.strip()
                if str != '':
                    self.command = str
                    return True

    def command_type(self):
        if A_COMMAND.match(self.command) != None:
            return 'A_COMMAND'
        elif C_COMMAND.match(self.command) != None:
            return 'C_COMMAND'
        elif L_COMMAND.match(self.command) != None:
            return 'L_COMMAND'
        else:
            raise Exception('Invalid command')

    def symbol(self):
        cmd_type = self.command_type()
        if cmd_type == 'A_COMMAND':
            return self.command[1:]
        elif cmd_type == 'L_COMMAND':
            return self.command[1:-1]

    def dest(self):
        m = C_COMMAND.match(self.command)
        return m.group(1) if m.group(1) != None else 'null'

    def comp(self):
        m = C_COMMAND.match(self.command)
        return m.group(2)

    def jump(self):
        m = C_COMMAND.match(self.command)
        return m.group(3) if m.group(3) != None else 'null'
