from lib.error import CompilerError
from lib.utils import is_int, is_number, is_operation, is_inttab, get_symbol, is_label, is_variable, symtab_sort


class Machine:
    slots = {
        'code',
        'mem',
        'labels',
        'num_cache',
        'free_index'
    }

    def __init__(self):
        self.labels = []
        self.code = []
        self.mem = {}
        self.num_cache = {}
        self.free_index = 0

    def reserve_memory(self, symtab):
        for i in range(10):
            self.mem[i] = str(i)

        for index, symbol in enumerate(symtab_sort(symtab), 10):
            self.mem[symbol] = index

        self.free_index = 10 + len(symtab)

    def set_labels(self, flow):
        for c in flow:
            if is_label(c) and c[1] not in self.labels:
                self.labels.append(c[1])

        sorted(self.labels)

    def get_new_label(self):
        current = int(sorted(self.labels, key=lambda l: int(l[5:]))[-1][5:]) if self.labels else 0
        self.labels.append('label{}'.format(current + 1))
        return self.labels[-1]

    def resolve_labels(self):
        resolved = []
        labels = {}

        for i, c in enumerate(self.code):
            if isinstance(c, tuple) and c[0] == 'label':
                labels[c[1]] = len(resolved)
            else:
                resolved.append(c)

        for i, c in enumerate(resolved):
            if isinstance(c, tuple):
                resolved[i] = '{} {}'.format(c[0], labels[c[1]])
        self.code = resolved
        print(str(self.mem))

    def generate_number(self, number, add=True):
        # code = []

        mem_addr = '#{}'.format(number)
        # mem_val = self.mem.get(mem_addr, False)
        #
        # if mem_val:
        #     code += ['LOAD {}'.format(mem_val)]
        # else:
        code = ['ZERO']

        if number != 0:
            number = bin(number)
            code += ['INC']
            for d in number[3:]:
                code += ['SHL']
                if d == '1':
                    code += ['INC']

        # self.mem[mem_addr] = self.free_index
        # code += ['STORE {}'.format(self.free_index)]
        #
        # self.free_index += 1
        if add:
            self.code += code
        return "\n".join(code)

    def assign(self, target, expression):
        _, *value = expression
        if is_operation(value):
            self.assign_operation(target, value)
        else:
            if is_variable(value[0]):
                self.assign_variable(target, value[0])
            elif is_number(value[0]):
                self.assign_number(target, value[0])
            else:
                raise CompilerError("Unknown value type")

    def assign_variable(self, target, source):
        code = """
        LOAD a
        STORE b
        """
        self.parse(code, a=source, b=target)

    def assign_number(self, target, source):
        self.generate_number(source)
        code = """
        STORE b
        """
        self.parse(code, b=target)

    def assign_operation(self, target, equation):
        sign, *operands = equation

        operations = {
            '+': self.operation_add,
            '-': self.operation_substract,
            '/': self.operation_divide,
            '*': self.operation_multiply,
            '%': self.operation_modulo
        }

        operations[sign](target, operands)

    def operation_add(self, target, operands):
        x, y = operands
        if is_number(x):
            # t := 1 + 1
            if is_number(y):
                self.generate_number(x + y)
            # t := 1 + a
            # t  := 1 + a[x]
            elif is_int(y) or is_inttab(y):
                self.generate_number(x)
                self.parse('ADD y', y=y)
        elif is_int(x) or is_inttab(x):
            # t := a + 1
            if is_number(y):
                x, y = y, x
                self.generate_number(x)
                self.parse('ADD y', y=y)
            # t := a + b
            # t := a + b[x]
            elif is_int(y) or is_inttab(y):
                self.parse('LOAD x', x=x)
                self.parse('ADD y', y=y)
            else:
                raise CompilerError("Unexpected symbol")

        self.parse('STORE a', a=target)

    def operation_substract(self, target, operands):
        x, y = operands
        if is_number(x):
            # t := 1 - 1
            if is_number(y):
                self.generate_number(x - y)
            # t := 1 - a
            # t := 1 - a[x]
            elif is_variable(y):
                self.generate_number(x)
                self.parse('SUB a', a=y)
        elif is_variable(x):
            # t := a - 1
            r0 = ('int', 0, 0)
            if is_number(y):
                self.generate_number(y)
                self.parse('STORE a', a=r0)
                self.parse('LOAD a', a=x)
                self.parse('SUB a', a=r0)
            # t := a - b
            # t := a - b[x]
            elif is_variable(y):
                self.parse('LOAD a', a=x)
                self.parse('SUB a', a=y)
            else:
                raise CompilerError("Unexpected symbol")
        self.parse('STORE a', a=target)

    def operation_multiply(self, target, operands):
        [left, right] = operands
        if is_variable(left):
            if is_variable(right):
                r0 = ('int', 0, 0)
                r1 = ('int', 1, 0)
                r2 = ('int', 2, 0)
                code = """
                ZERO
                STORE r2
                LOAD x
                STORE r0
                LOAD y
                STORE r1
    
                #START:
                
                LOAD r1
                JZERO #END
                JODD #IS_ODD
                JUMP #NOT_ODD
                
                #IS_ODD:
                
                LOAD r2
                ADD r0
                STORE r2
                
                #NOT_ODD:
                
                LOAD r1
                SHR
                STORE r1
                LOAD r0
                SHL
                STORE r0
                
                JUMP #START
                
                #END:
                LOAD r2
                STORE z
                """

                self.parse(code,
                           r0=r0,
                           r1=r1,
                           r2=r2,
                           x=left,
                           y=right,
                           z=target)

    def operation_divide(self, target, operands):
        [left, right] = operands

        if is_variable(right):
            if is_variable(left):
                r0, r1, r2, r3 = (('int', i, i) for i in range(4))
                code = """
                        ZERO
                        STORE r2
                        LOAD x
                        STORE r0
                        LOAD y
                        STORE r1
                        STORE r3

                        #SHIFT:
                        LOAD r1
                        SHL
                        STORE r1
                        LOAD r0
                        INC
                        SUB r1
                        JZERO #ADJUST
                        JUMP #SHIFT

                        #ADJUST:
                        LOAD r1
                        SHR
                        STORE r1
                        
                        #LOOP:
                        LOAD r3
                        SUB r1
                        JZERO #DIVISION
                        JUMP #END
                        
                        #DIVISION:
                        LOAD r1
                        SUB r0
                        JZERO #ADD
                        JUMP #NO_ADD
                        
                        #ADD:
                        LOAD r2
                        SHL
                        INC
                        STORE r2
                        LOAD r0
                        SUB r1
                        STORE r0
                        LOAD r1
                        SHR
                        STORE r1
                        JUMP #LOOP
                        
                        #NO_ADD:
                        LOAD r2
                        SHL
                        STORE r2
                        LOAD r1
                        SHR
                        STORE r1
                        JUMP #LOOP
                        
                        #END:
                        LOAD r2
                        STORE z
                        """
                self.parse(code,
                           x=left,
                           y=right,
                           z=target, r0=r0, r1=r1, r2=r2, r3=r3)

    def operation_modulo(self, target, operands):
        [left, right] = operands

        if is_variable(right):
            if is_variable(left):
                r0, r1, r2, r3 = (('int', i, i) for i in range(4))
                code = """
                        ZERO
                        STORE r2
                        LOAD x
                        STORE r0
                        LOAD y
                        STORE r1
                        STORE r3

                        #SHIFT:
                        LOAD r1
                        SHL
                        STORE r1
                        LOAD r0
                        INC
                        SUB r1
                        JZERO #ADJUST
                        JUMP #SHIFT

                        #ADJUST:
                        LOAD r1
                        SHR
                        STORE r1

                        #LOOP:
                        LOAD r3
                        SUB r1
                        JZERO #DIVISION
                        JUMP #END

                        #DIVISION:
                        LOAD r1
                        SUB r0
                        JZERO #ADD
                        JUMP #NO_ADD

                        #ADD:
                        LOAD r2
                        SHL
                        INC
                        STORE r2
                        LOAD r0
                        SUB r1
                        STORE r0
                        LOAD r1
                        SHR
                        STORE r1
                        JUMP #LOOP

                        #NO_ADD:
                        LOAD r2
                        SHL
                        STORE r2
                        LOAD r1
                        SHR
                        STORE r1
                        JUMP #LOOP

                        #END:
                        LOAD r0
                        STORE z
                        """
                self.parse(code,
                           x=left,
                           y=right,
                           z=target, r0=r0, r1=r1, r2=r2, r3=r3)

    def write(self, value):
        if is_variable(value):
            self.write_variable(value)
        else:
            self.write_number(value)

    def write_variable(self, source):
        code = """
        LOAD a
        PUT"""
        self.parse(code, a=source)

    def write_number(self, value):
        self.generate_number(value)
        self.parse('PUT')

    def read(self, target):
        if is_variable(target):
            self.read_variable(target)
        else:
            raise CompilerError("Cannot READ non-variable")

    def read_variable(self, target):
        code = """
        GET
        STORE a
        """
        self.parse(code, a=target)

    def comp(self, cmd):
        _, cond, _, label = cmd
        comps = {
            '=':  self.comp_eq,
            '<>': self.comp_neq,
            '>':  self.comp_gt,
            '>=': self.comp_geq,
            '<=': self.comp_leq,
            '<':  self.comp_lt

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
                self.parse(code, a=left, b=right, label=label)
            elif is_number(right):
                # a = 1
                if right == 0:
                    code = """
                    LOAD a
                    JZERO @label
                    """
                    self.parse(code, a=left, label=label)
                elif right == 1:
                    code = """
                    LOAD a
                    JZERO #FALSE
                    DEC
                    JZERO @label
                    #FALSE:
                    """
                    self.parse(code, a=left, label=label)
                else:
                    raise CompilerError("Not implemented yet")
            else:
                raise CompilerError()
        else:
            raise CompilerError("Not implemented")
            # TODO: implement for numbers

    def comp_neq(self, cond, label):
        left, _, right = cond

        if is_variable(right):
            left, right = right, left

        if is_variable(left):
            if is_variable(right):
                code = """
                LOAD a
                SUB b
                JZERO #FALSE1
                JUMP @true
                #FALSE1:
                LOAD b
                SUB a
                JZERO #FALSE
                JUMP @true
                #FALSE:"""
                self.parse(code, a=left, b=right, true=label)
            elif is_number(right):
                raise CompilerError("Not implemented yet")

        if is_number(left) and is_number(right):
            if left != right:
                self.parse('JUMP @true', true=label)

        raise CompilerError("Not implemented yet")

    def comp_gt(self, cond, label):
        left, _, right = cond

        if is_variable(right):
            if is_variable(left):
                code = """
                LOAD a
                SUB b
                JZERO #FALSE
                JUMP @label
                #FALSE:
                """
                self.parse(code, a=left, b=right, label=label)
            raise CompilerError("Not implemented yet")
        raise CompilerError("Not implemented yet")

    def comp_geq(self, cond, label):
        left, _, right = cond

        if is_variable(right):
            if is_variable(left):
                code = """
                LOAD a
                INC
                SUB b
                JZERO #FALSE
                JUMP @true
                #FALSE:
                """
                self.parse(code, a=left, b=right, true=label)

            raise CompilerError("Not implemented yet")
        raise CompilerError("Not implemented yet")

    def comp_lt(self, cond, label):
        self.comp_gt((cond[2], '>', cond[0]), label)

    def comp_leq(self, cond, label):
        self.comp_geq((cond[2], '<=', cond[0]), label)

    def parse(self, code, **variables):
        """
        JZERO #LABEL1   <-    # make new label
        JZERO @label    <-    @ use existing label
        #LABEL:         <-    label placement (one only)
        """
        # TODO: now I assume there are only variables, no numbers
        labels = {}
        for c in [c.strip() for c in code.split("\n") if c.strip() != '']:
            left, right = (c.split(" ") + [None])[:2]
            if not right and left[1:-1] not in labels.keys() and left[0] == '#':
                # for new labels, generate unique labels names
                label_name = self.get_new_label()
                labels[left[1:-1]] = label_name
                # parse found label to ('label', tuple)
                self.code.extend([('label', label_name), ])
            elif not right and left[0] == '#':
                # if new label, but unique name already generated
                self.code.extend([('label', labels[left[1:-1]]), ])
            elif not right:
                self.code.extend([left])
            elif right in variables.keys():
                # replace name with address
                variable = variables[right]
                if is_inttab(variable):
                    self.parse_array(left, variable)
                elif is_number(variable):
                    self.parse_number(left, variable)
                    if out: self.code.append(out)
                else:
                    resolved = variable[1]
                    self.code.extend(['{cmd} {param}'.format(
                        cmd=left,
                        param=self.mem[resolved])])
            elif right[0] == '#' and right[1:] not in labels.keys():
                # new label, but as JUMP (kind of)
                label_name = self.get_new_label()
                labels[right[1:]] = label_name
                self.code.extend([(left, label_name), ])
            elif right[0] == '#':
                # not new label, but as JUMP (kind of)
                self.code.extend([(left, labels[right[1:]]), ])
            elif right[0] == '@':
                # old label, replace with real name provided as kwarg
                self.code.extend([(left, variables[right[1:]]), ])
            else:
                self.code.extend([('{cmd} {param}'.format(
                    cmd=left,
                    param=right),)])

    def parse_array(self, left, right):
        _, var, index = right
        if is_number(index):
            addr = '{}#{}'.format(var, index)
            code = '{cmd} {param}'.format(
                cmd=left,
                param=self.mem[addr])
            self.code.append(code)
        elif is_variable(index):
            left += 'I'
            arr_addr = self.mem['{}#0'.format(var)]
            r9 = ('int', 9, 9)
            r8 = ('int', 8, 8)
            if left == 'LOADI':
                self.generate_number(arr_addr)
                code = """
                ADD x
                STORE r9
                LOADI r9
                """
                self.parse(code, x=index, r9=r9)
            elif left == 'STOREI':
                code = """
                STORE r9
                """
                code += self.generate_number(arr_addr, add=False)
                code += """
                ADD x
                STORE r8
                LOAD r9
                STOREI r8
                """
                self.parse(code, x=index, r9=r9, r8=r8)
            elif left == 'ADDI':
                code = """
                STORE r9
                """
                code += self.generate_number(arr_addr, add=False)
                code += """
                ADD x
                STORE r8
                LOAD r9
                ADDI r8
                """
                self.parse(code, x=index, r9=r9, r8=r8)
            elif left == 'SUBI':
                # TODO: fix substraction for arrays!
                code = """
                STORE r9
                """
                code += self.generate_number(arr_addr, add=False)
                code += """
                ADD x
                STORE r8
                LOAD r9
                SUBI r8
                """
                self.parse(code, x=index, r9=r9, r8=r8)

    def parse_number(self, left, right):
        if left == 'SUB':
            r0 = ('int', 0, 0)
            r1 = ('int', 1, 1)
            code = """
            STORE r0
            """
            code += self.generate_number(right, add=False)
            code += """
            STORE r1
            LOAD r0
            SUB r1
            """
            self.parse(code, r0=r0, r1=r1)
        else:
            import pdb;
            pdb.set_trace()

    def end(self):
        self.parse('HALT')
