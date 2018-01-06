from lib.error import CompilerError
from lib.utils import is_int, is_number, is_operation, is_inttab, is_label, is_variable, symtab_sort


class Reg:
    r0 = ('int', 0, 0)
    r1 = ('int', 1, 1)
    r2 = ('int', 2, 2)
    r3 = ('int', 3, 3)
    r4 = ('int', 4, 4)
    r5 = ('int', 5, 5)
    r6 = ('int', 6, 6)
    r7 = ('int', 7, 7)
    r8 = ('int', 8, 8)
    r9 = ('int', 9, 9)


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
        mem_addr = 10

        for symbol in symtab_sort(symtab):
            if symbol[0] != '#' and '#' in symbol:
                symbol, size = symbol.split('#')
                size = int(size)
                self.mem[symbol + '#0'] = {
                    'address': mem_addr,
                    'size':    size
                }
                mem_addr += size
            else:
                self.mem[symbol] = mem_addr
                mem_addr += 1

        self.free_index = mem_addr

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

    def generate_number(self, number):
        code = ['ZERO']

        if number != 0:
            number = bin(number)
            code += ['INC']
            for d in number[3:]:
                code += ['SHL']
                if d == '1':
                    code += ['INC']

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
        code = """
        GENERATE n
        STORE b
        """
        self.parse(code, n=source, b=target)

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
            if is_number(y):
                self.parse('GENERATE n', n=x + y)
            else:
                x, y = y, x

        if is_int(x) or is_inttab(x):
            # t := a + 1
            if is_number(y):
                if y <= 1:
                    self.parse('LOAD x', x=x)
                    for _ in range(y):
                        self.parse('INC')
                else:
                    self.parse('GENERATE n', n=y)
                    self.parse('ADD x', x=x)
            # t := a + b
            # t := a + b[x]
            elif is_variable(y):
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
                self.parse('GENERATE n', n=x - y)
            # t := 1 - a
            # t := 1 - a[x]
            elif is_variable(y):
                self.parse('GENERATE n', n=x)
                self.parse('SUB a', a=y)
        elif is_variable(x):
            # t := a - 1
            if is_number(y):
                # TODO: check what's faster
                if y == 0:
                    self.parse('LOAD a', a=x)
                elif y == 1:
                    self.parse('LOAD a', a=x)
                    self.parse('DEC')
                else:
                    self.parse('GENERATE n', n=y)
                    self.parse('STORE a', a=Reg.r0)
                    self.parse('LOAD x', x=x)
                    self.parse('SUB a', a=Reg.r0)
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

        code = ""

        if is_number(left):
            code += """
                   GENERATE l_val
                   STORE left
                   """

        if is_number(right):
            code += """
                   GENERATE r_val
                   STORE right
                   """

        code += """
            ZERO
            STORE r2
            LOAD left
            STORE r0
            LOAD right
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
            STORE target
            """

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   r0=Reg.r0,
                   r1=Reg.r1,
                   r2=Reg.r2,
                   left=left if is_variable(left) else Reg.r4,
                   right=right if is_variable(right) else Reg.r5,
                   target=target)

    def operation_divide(self, target, operands):
        self.operation_divmod(target, operands)

    def operation_modulo(self, target, operands):
        self.operation_divmod(target, operands, division=False)

    def operation_divmod(self, target, operands, division=True):
        [left, right] = operands

        # 0 -> r2
        code = """
               ZERO
               STORE r2"""
        # x -> r0
        code += """
               GENERATE l_val
               """ if is_number(left) else """
               LOAD left
               """
        code += """
               STORE r0
               """
        # y -> r1, r3
        code += """
               GENERATE r_val
               """ if is_number(right) else """
               LOAD right
               """
        code += """
               JZERO #END_ZERO
               STORE r1
               STORE r3
               """

        code += """
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

               #END_ZERO:
               LOAD r2
               STORE target
               JUMP #WAS_ZERO
               
               #END:
               LOAD {target_reg}
               STORE target
               #WAS_ZERO:
               """.format(target_reg='r2' if division else 'r0')

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   left=left if is_variable(left) else Reg.r4,
                   right=right if is_variable(right) else Reg.r5,
                   target=target,
                   r0=Reg.r0, r1=Reg.r1, r2=Reg.r2, r3=Reg.r3)

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
        self.parse('GENERATE n', n=value)
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
        code = ""

        if is_number(left) and is_number(right):
            if left != right:
                return

        if is_number(right):
            right, left = left, right

        if left == right:
            self.parse('JUMP @label', label=label)
            return

        if is_number(left) and left == 0:
            code = """
            LOAD a
            JZERO @label
            """
            self.parse(code, a=right, label=label)
            return

        if is_number(left):
            code += """
            GENERATE l_val
            STORE left
            """

        if is_number(right):
            code += """
            GENERATE r_val
            STORE right
            """

        code += """
        LOAD left
        SUB right
        JZERO #LABEL1
        JUMP #FALSE
        #LABEL1:
        LOAD right
        SUB left
        JZERO @label
        #FALSE:
        """

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   left=left if is_variable(left) else Reg.r0,
                   right=right if is_variable(right) else Reg.r1,
                   label=label
                   )

    def comp_neq(self, cond, label):
        left, _, right = cond

        if is_number(left) and is_number(right):
            if left == right:
                return
            else:
                self.parse('JUMP @label', label=label)
                return

        if is_number(right):
            right, left = left, right

        if not is_number(right) and is_number(left) and left == 0:
            code = """
            LOAD a
            JZERO #FALSE
            JUMP @label
            #FALSE:
            """
            self.parse(code, a=right, label=label)
            return

        code = ""

        if is_number(left):
            code += """
               GENERATE l_val
               STORE left
               """

        if is_number(right):
            code += """
               GENERATE r_val
               STORE right
               """

        code += """
            LOAD left
            SUB right
            JZERO #FALSE1
            JUMP @label
            #FALSE1:
            LOAD right
            SUB left
            JZERO #FALSE
            JUMP @label
            #FALSE:
            """

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   left=left if is_variable(left) else Reg.r0,
                   right=right if is_variable(right) else Reg.r1,
                   label=label
                   )

    def comp_gt(self, cond, label):
        left, _, right = cond
        code = ""

        if is_number(left):
            code += """
            GENERATE l_val
            STORE left
            """

        if is_number(right):
            code += """
            GENERATE r_val
            STORE right
            """

        code += """
        LOAD left
        SUB right
        JZERO #FALSE
        JUMP @label
        #FALSE:
        """

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   left=left if is_variable(left) else Reg.r0,
                   right=right if is_variable(right) else Reg.r1,
                   label=label
                   )

    def comp_geq(self, cond, label):
        left, _, right = cond

        if is_number(right) and right == 0:
            self.parse("JUMP @label", label=label)
            return

        code = ""
        if is_number(left):
            code += """
            GENERATE l_val
            STORE left
            """

        if is_number(right):
            code += """
            GENERATE r_val
            STORE right
            """

        code += """
        LOAD left
        INC
        SUB right
        JZERO #FALSE
        JUMP @label
        #FALSE:
        """

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   left=left if is_variable(left) else Reg.r0,
                   right=right if is_variable(right) else Reg.r1,
                   label=label
                   )

    def comp_lt(self, cond, label):
        left, _, right = cond
        self.comp_gt((right, '>', left), label)

    def comp_leq(self, cond, label):
        left, _, right = cond
        self.comp_geq((right, '<=', left), label)

    def parse(self, code, **variables):
        """
        JZERO #LABEL1   <-    # make new label
        JZERO @label    <-    @ use existing label
        #LABEL:         <-    label placement (one only)
        """
        labels = {}
        for c in [c.strip() for c in code.split("\n") if c.strip() != '']:
            left, right = (c.split(" ") + [None])[:2]
            if left == 'GENERATE':
                number = int(variables[right])
                cmds = self.generate_number(number).split('\n')
                self.code.extend(cmds)
            elif not right and left[1:-1] not in labels.keys() and left[0] == '#':
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
        _, var, index, *_ = right
        if is_number(index):
            array = self.mem['{}#0'.format(var)]
            arr_addr = array['address']
            cell_addr = index + arr_addr
            code = '{cmd} {param}'.format(
                cmd=left,
                param=cell_addr)
            self.code.append(code)
        elif is_variable(index):
            left += 'I'
            array = self.mem['{}#0'.format(var)]
            arr_addr = array['address']
            if left == 'LOADI':
                code = """
                GENERATE num
                ADD x
                STORE r9
                LOADI r9
                """
                self.parse(code, num=arr_addr, x=index, r9=Reg.r9)
            elif left in ['STOREI', 'ADDI', 'SUBI']:
                code = """
                STORE r8
                GENERATE num
                ADD x
                STORE r9
                LOAD r8
                {cmd} r9
                """.format(cmd=left)
                self.parse(code, num=arr_addr, x=index, r9=Reg.r9, r8=Reg.r8)
            else:
                raise CompilerError("Unexpected command")

    def end(self):
        self.parse('HALT')
