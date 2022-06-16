a_cmd_dict = {
    'add' : '+',
    'sub' : '-',
    'neg' : '-',
    'eq'  : 'JEQ',
    'gt'  : 'JGT',
    'lt'  : 'JLT',
    'and' : '&',
    'or'  : '|',
    'not' : '!',
}

seg_cmd_dict = {
    'constant' :lambda i: '@'+str(i),
    'argument' :'@ARG',
    'local'    :'@LCL',
    'this'     :'@THIS',
    'that'     :'@THAT',
    'pointer'  :lambda i: '@R'+str(3+i),
    'temp'     :lambda i: '@R'+str(5+i),
    'static'   :lambda i, f: '@R'+f+'.'+str(i)
}

class CodeWriter:

    def __init__(self, file):
        self.f = open(file, 'w')
        self.label_num = 0

    def set_file_name(self, file_name):
        self.file_name = file_name
    
    def write_arithmetic(self, command):
        if command in ['neg', 'not']:
            assembly = [
                '@SP',
                'A=M-1',
                'M=' + a_cmd_dict[command] + 'M',
            ]
        else:
            assembly = self.pop()
            assembly.append('D=M')
            assembly += self.pop()
            if command in ['add', 'and', 'or']:
                assembly.append('D=D' + a_cmd_dict[command] + 'M')
            elif command == 'sub':
                assembly.append('D=M' + a_cmd_dict[command] + 'D')
            else:
                label_1 = self.get_label_name()
                label_2 = self.get_label_name()
                assembly += [
                    'D=M-D',
                    '@' + label_1,
                    'D;' + a_cmd_dict[command],
                    'D=0',
                    '@' + label_2,
                    '0;JMP',
                    '(' + label_1 + ')',
                    'D=-1',
                    '('+ label_2 + ')',
                ]
            assembly += self.push()
        self.write_assembly(assembly)        
            
    def write_push_pop(self, command, segment, index):
        if command == 'C_PUSH':
            if segment == 'constant':
                assembly = [
                    seg_cmd_dict[segment](index),
                    'D=A',
                ]
            elif segment in ['argument', 'local', 'this', 'that']:
                assembly = [
                    seg_cmd_dict[segment],
                    'A=M',
                ]
                assembly += ['A=A+1'] * index + ['D=M']
            elif segment in ['pointer', 'temp']:
                assembly = [
                    seg_cmd_dict[segment](index),
                    'D=M',
                ]
            elif segment == 'static':
                assembly = [
                    seg_cmd_dict[segment](index, self.file_name),
                    'D=M',
                ]
            assembly += self.push()
        elif command == 'C_POP':
            assembly = self.pop()
            assembly.append('D=M')
            if segment in ['argument', 'local', 'this', 'that']:
                assembly += [
                    seg_cmd_dict[segment],
                    'A=M',
                ]
                assembly += ['A=A+1'] * index
            elif segment in ['pointer', 'temp']:
                assembly.append(seg_cmd_dict[segment](index))
            elif segment == 'static':
                assembly.append(seg_cmd_dict[segment](index, self.file_name))
            assembly.append('M=D')
        self.write_assembly(assembly)

    def close(self):
        self.f.close()

    def push(self):
        return [
            '@SP',
            'A=M',
            'M=D',
            '@SP',
            'M=M+1',
        ]

    def pop(self):
        return [
            '@SP',
            'M=M-1',
            'A=M'
        ]

    def move(self, index):
        return ['A=A+1'] * index

    def get_label_name(self):
        label_name = 'LABEL'+str(self.label_num)
        self.label_num += 1
        return label_name

    def write_assembly(self, assembly):
        assembly = map(lambda x: x+'\n', assembly)
        self.f.writelines(assembly)
