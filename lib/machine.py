class Machine:
    def __init__(self):
        self.reg = None
        self.code = []
        self.mem = {}

    def reserve_memory(self, symtab):
        for index, symbol in enumerate(symtab, 10):
            self.mem[symbol] = index

    def number(self, source):
        code = ['ZERO']

        if source != 0:
            num = bin(source)
            code += ['INC']
            for d in num[3:]:
                code += ['SHL']
                if d == '1':
                    code += ['INC']

        self.code += code

    def assign(self, variable, expression):
        _, *value = expression
        if len(value) == 1:
            if isinstance(value[0], tuple):
                self.assign_variable(variable, value[0])
            else:
                self.assign_number(variable, value[0])
        else:
            self.assign_operation(variable, value)

    def assign_variable(self, target, source):
        pass

    def assign_number(self, target, source):
        self.number(source)
        code = ['STORE {}'.format(self.mem[target[1]])]
        self.mem[target] = source
        self.code += code

    def assign_operation(self, target, equation):
        operations = {
            '+': lambda x, y: self.operation_add(x, y)
        }
        operations[equation[0]](equation[1], equation[2])

    def operation_add(self, left_operand, right_operand):
        import pdb; pdb.set_trace()
        pass

    def write(self, value):
        if isinstance(value, tuple):
            self.write_variable(value)
        else:
            self.write_number(value)

    def write_variable(self, variable):
        code = ['LOAD {}'.format(self.mem[variable[1]])]
        code += ['PUT']
        self.code += code

    def write_number(self, value):
        self.number(value)
        code = ['PUT']
        self.code += code

    def end(self):
        self.code += ['HALT']


