from lib.error import CompilerError
from lib.utils import is_int, is_number, is_operation, is_inttab, get_symbol, is_label, is_variable


class Machine:
    slots = {
        'code',
        'mem',
        'labels'
    }

    def __init__(self):
        self.code = []
        self.mem = {}
        self.labels = []

    def set_labels(self, flow):
        for c in flow:
            if is_label(c) and c[1] not in self.labels:
                self.labels.append(c[1])
        sorted(self.labels)

    def get_new_label(self):
        current = int(sorted(self.labels)[-1][5:])
        self.labels.append('label{}'.format(current + 1))
        return self.labels[-1]

    def resolve_labels(self):
        resolved = []
        labels = {}

        for i, c in enumerate(self.code):
            if isinstance(c, tuple) and c[0] == 'label':
                # resolved[-1] = ('label', c[1], resolved),
                labels[c[1]] = len(resolved)
            else:
                resolved.append(c)

        for i, c in enumerate(resolved):
            if isinstance(c, tuple):
                resolved[i] = '{} {}'.format(c[0], labels[c[1]])
        self.code = resolved

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
            elif is_variable(y):
                self.set_number_in_register(x)
                self.sub_memory_from_register(y)
        elif is_variable(x):
            # t := a - 1
            if is_number(y):
                self.set_number_in_register(y)
                self.save_register_to_memory(0)
                self.set_memory_in_register(x)
                self.sub_memory_from_register(0)
            # t := a - b
            # t := a - b[x]
            elif is_variable(y):
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

    def check_if(self, cmd):
        _, cond, _, label = cmd
        comps = {
            '=': self.comp_eq
        }
        comps[cond[1]](cond, label)

    def comp_eq(self, cond, label):
        left, _, right = cond
        if is_variable(right):
            left, right = right, left

        if is_variable(left):
            # now left must be an int
            if is_variable(right):
                # two ints
                code = """
                LOAD a
                SUB b
                JZERO #LABEL1
                JUMP #FALSE
                #LABEL1:
                LOAD b
                SUB a
                JZERO @label
                #FALSE:
                """
                self.code_to_cmds(code,
                                  a=left,
                                  b=right,
                                  label=label)
            elif is_number(right):
                # a = 1
                if right == 0:
                    code = """
                    LOAD a
                    JZERO @label
                    """
                    self.code_to_cmds(code,
                                      a=left,
                                      label=label)
            else:
                raise CompilerError()
        else:
            import pdb;
            pdb.set_trace()
            raise CompilerError("Not implemented")
            # TODO: implement for numbers

    def code_to_cmds(self, code, **variables):
        """
        JZERO #LABEL1   <-    # make new label
        JZERO @label    <-    @ use existing label
        #LABEL:         <-    label placement (one only)
        """
        # TODO: now I assume there are only variables, no numbers
        labels = {}
        cmds = []
        for c in [c.strip() for c in code.split("\n") if c.strip() != '']:
            left, right = (c.split(" ") + [None])[:2]
            if not right and left[1:-1] not in labels.keys():
                # for new labels, generate unique labels names
                label_name = self.get_new_label()
                labels[left[1:-1]] = label_name
                # parse found label to ('label', tuple)
                cmds.append(('label', label_name), )
            elif not right:
                # if new label, but already parsed
                cmds.append(('label', labels[left[1:-1]]), )
            elif right in variables.keys():
                # replace name with address
                resolved = variables[right][1]
                cmds.append('{cmd} {param}'.format(
                    cmd=left,
                    param=self.mem[resolved]),
                )
            elif right[0] == '#':
                # new label, but as JUMP (kind of)
                label_name = self.get_new_label()
                labels[right[1:]] = label_name
                cmds.append((left, label_name), )
            elif right[0] == '@':
                # old label, replace with real name provided as kwarg
                cmds.append((left, variables[right[1:]]), )
            else:
                cmds.append('{cmd} {param}'.format(
                    cmd=left,
                    param=right),
                )
        self.code.extend(cmds)
