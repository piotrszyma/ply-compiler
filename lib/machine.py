from lib.error import CompilerError
from lib.utils import is_int, is_number, is_operation, is_inttab, get_symbol


class Machine:
    def __init__(self):
        self.code = []
        self.mem = {}

    def reserve_memory(self, symtab):
        for i in range(10):
            self.mem[i] = str(i)

        for index, symbol in enumerate(symtab, 10):
            self.mem[symbol] = index

    def generate_number_in_register(self, number):
        code = ['ZERO']

        if number != 0:
            number = bin(number)
            code += ['INC']
            for d in number[3:]:
                code += ['SHL']
                if d == '1':
                    code += ['INC']

        self.code += code

    def save_register_in_swap_mem(self, index):
        if 0 < index < 9:
            self.code += ['STORE {}'.format(index)]
        else:
            raise CompilerError("Swap mem out of range")

    def load_to_register_from_swap_mem(self, index):
        if 0 < index < 9:
            self.code += ['LOAD {}'.format(index)]
        else:
            raise CompilerError("Swap mem out of range")

    def set_number_in_register(self, number):
        self.generate_number_in_register(number)

    def set_memory_in_register(self, source):
        symbol = get_symbol(source)
        self.code += ['LOAD {}'.format(self.get_addr(symbol))]

    def add_memory_to_register(self, source):
        symbol = get_symbol(source)
        self.code += ['ADD {}'.format(self.get_addr(symbol))]

    def sub_memory_from_register(self, source):
        symbol = get_symbol(source)
        self.code += ['SUB {}'.format(self.get_addr(symbol))]

    def save_register_to_memory(self, target):
        symbol = get_symbol(target)
        self.code += ['STORE {}'.format(self.get_addr(symbol))]

    def get_addr(self, symbol):
        return self.mem[symbol]

    def assign(self, target, expression):
        _, *value = expression
        import pdb; pdb.set_trace()
        if is_operation(value):
            self.assign_operation(target, value)
        else:
            if is_int(value[0]):
                self.assign_variable(target, value[0])
            elif is_number(value[0]):
                self.assign_number(target, value[0])
            else:
                raise CompilerError("Unknown value type")

    def assign_variable(self, target, source):
        self.set_memory_in_register(source)
        self.save_register_to_memory(target)

    def assign_number(self, target, source):
        self.generate_number_in_register(source)
        self.save_register_to_memory(target)

    def assign_operation(self, target, equation):
        sign, *operands = equation

        operations = {
            '+': lambda x, y: self.operation_add(x, y),
            '-': lambda x, y: self.operation_substract(x, y),
            '/': lambda x, y: self.operation_divide(x, y),
            '*': lambda x, y: self.operation_multiply(x, y),
            '%': lambda x, y: self.operation_modulo(x, y)
        }

        operations[sign](target, operands)

    def operation_add(self, target, operands):
        x, y = operands
        if is_number(x):
            # t := 1 + 1
            if is_number(y):
                self.generate_number_in_register(x + y)
            # t := 1 + a
            # t  := 1 + a[x]
            elif is_int(y) or is_inttab(y):
                self.set_number_in_register(x)
                self.add_memory_to_register(y)
        elif is_int(x) or is_inttab(x):
            # t := a + 1
            if is_number(y):
                x, y = y, x
                self.set_number_in_register(x)
                self.add_memory_to_register(y)
            # t := a + b
            # t := a + b[x]
            elif is_int(y) or is_inttab(y):
                self.set_memory_in_register(x)
                self.add_memory_to_register(y)
            else:
                raise CompilerError("Unexpected symbol")

        self.save_register_to_memory(target)

    def operation_substract(self, target, operands):
        x, y = operands
        if is_number(x):
            # t := 1 - 1
            if is_number(y):
                self.generate_number_in_register(x - y)
            # t := 1 - a
            # t := 1 - a[x]
            elif is_int(y) or is_inttab(y):
                self.set_number_in_register(x)
                self.sub_memory_from_register(y)
        elif is_int(x) or is_inttab(x):
            # t := a - 1
            if is_number(y):
                self.set_number_in_register(y)
                self.save_register_to_memory(0)
                self.set_memory_in_register(x)
                self.sub_memory_from_register(0)
            # t := a - b
            # t := a - b[x]
            elif is_int(y) or is_inttab(y):
                self.set_memory_in_register(x)
                self.sub_memory_from_register(y)
            else:
                raise CompilerError("Unexpected symbol")

        self.save_register_to_memory(target)

    def operation_divide(self, target, operands):
        pass

    def operation_multiply(self, target, operands):
        pass

    def operation_modulo(self, target, operands):
        pass

    def write(self, value):
        if isinstance(value, tuple):
            self.write_variable(value)
        else:
            self.write_number(value)

    def write_variable(self, source):
        symbol = get_symbol(source)
        code = ['LOAD {}'.format(self.get_addr(symbol))]
        code += ['PUT']
        self.code += code

    def write_number(self, value):
        self.generate_number_in_register(value)
        code = ['PUT']
        self.code += code

    def end(self):
        self.code += ['HALT']
