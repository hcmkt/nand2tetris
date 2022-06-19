cmd_dict = {
    'add':'C_ARITHMETIC',
    'sub':'C_ARITHMETIC',
    'neg':'C_ARITHMETIC',
    'eq':'C_ARITHMETIC',
    'gt':'C_ARITHMETIC',
    'gt':'C_ARITHMETIC',
    'lt':'C_ARITHMETIC',
    'and':'C_ARITHMETIC',
    'or':'C_ARITHMETIC',
    'not':'C_ARITHMETIC',
    'push':'C_PUSH',
    'pop':'C_POP',
    'label':'C_LABEL',
    'goto':'C_GOTO',
    'if-goto':'C_IF',
    'function':'C_FUNCTION',
    'return':'C_RETURN',
    'call':'C_CALL',
}

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
            str = str.strip(' ')
            if str == '':
                return False
            else:
                str = str[0:str.find('//')]
                if str != '':
                    self.command = str
                    return True
    
    def command_type(self):
        cmd = self.command.split()[0]
        return cmd_dict[cmd]

    def arg1(self):
        cmd_kind = self.command_type()
        if cmd_kind == 'C_RETURN':
            raise Exception('Error')
        if cmd_kind == 'C_ARITHMETIC':
            return self.command.split()[0]
        else:
            return self.command.split()[1]
    
    def arg2(self):
        cmd_kind = self.command_type()
        if cmd_kind not in ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']:
            raise Exception('Error')
        return int(self.command.split()[2])
