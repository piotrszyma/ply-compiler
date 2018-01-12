from math import sqrt, log

from lib.error import CompilerError
from lib.utils import is_int, is_number, is_operation, is_array, is_label, is_variable, symtab_sort, is_reg


class Reg:
    r0 = ('reg', 0, 0)
    r1 = ('reg', 1, 1)
    r2 = ('reg', 2, 2)
    r3 = ('reg', 3, 3)
    r4 = ('reg', 4, 4)
    r5 = ('reg', 5, 5)
    r6 = ('reg', 6, 6)
    r7 = ('reg', 7, 7)
    r8 = ('reg', 8, 8)
    r9 = ('reg', 9, 9)
    r10 = ('reg', 10, 10)  # used for storing array index
    r11 = ('reg', 11, 11)  #
    r12 = ('reg', 12, 12)  #


class Machine:
    slots = {
        'code',
        'mem',
        'labels',
        'free_index'
    }

    def __init__(self):
        self.labels = []
        self.code = []
        self.mem = {}
        self.free_index = 0

    def reserve_memory(self, symtab):
        for i in range(13):
            self.mem[i] = str(i)
        mem_addr = 13

        for symbol in symtab_sort(symtab):
            if symbol[0] != '#' and '#' in symbol:
                symbol, size = symbol.split('#')
                size = int(size)
                self.mem[symbol + '#0'] = {
                    'address':   mem_addr + 1,  # at the beginning store value of start address
                    'size':      size,
                    'start_ptr': mem_addr
                }
                mem_addr += size + 1
            else:
                self.mem[symbol] = mem_addr
                mem_addr += 1

        self.free_index = mem_addr

        for symbol, details in self.mem.items():
            if isinstance(symbol, str) and symbol[-2:] == '#0':
                self.parse("GENERATE address", address=details['address'])
                self.code.append("STORE {}".format(details['start_ptr']))

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

    def addr_to_reg_if_arr(self, source, register):
        if is_array(source) and is_int(source[2]):
            _, symbol, index, lineno = source
            self.code.append('LOAD {}'.format(self.mem[symbol + '#0']['start_ptr']))
            self.parse("""
            ADD index
            STORE reg
            """, index=index, reg=register)
            return 'int[]', symbol, register, lineno
        else:
            return source

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
        source = self.addr_to_reg_if_arr(source, Reg.r10)
        target = self.addr_to_reg_if_arr(target, Reg.r11)

        code = """
        LOAD a
        STORE b
        """
        self.parse(code, a=source, b=target)

    def assign_number(self, target, source):
        target = self.addr_to_reg_if_arr(target, Reg.r1)

        code = """
        GENERATE n
        STORE b
        """
        self.parse(code, n=source, b=target)

    def assign_operation(self, target, equation):
        sign, *operands = equation

        [left, right] = operands

        left = self.addr_to_reg_if_arr(left, Reg.r10)
        right = self.addr_to_reg_if_arr(right, Reg.r11)
        target = self.addr_to_reg_if_arr(target, Reg.r12)

        operands = [left, right]

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

        if is_array(x) and is_array(y):
            pass

        if is_number(x):
            if is_number(y):
                self.parse('GENERATE n', n=x + y)
                self.parse('STORE t', t=target)
                return
            else:
                x, y = y, x

        # t := a + 1
        if is_number(y):
            if y == 0:
                self.parse('LOAD x', x=x)
            elif y == 1:
                self.parse('LOAD x', x=x)
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
                if x - y > 0:
                    self.parse('GENERATE n', n=x - y)
                else:
                    self.parse('ZERO')
            # t := 1 - a
            # t := 1 - a[x]
            elif is_variable(y):
                self.parse('GENERATE n', n=x)
                self.parse('SUB a', a=y)
        elif is_variable(x):
            # t := a - 1
            if is_number(y):
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

        if is_number(right):
            left, right = right, left

        if is_number(left) and is_number(right):
            self.parse('GENERATE n', n=left * right)
            self.parse('STORE t', t=target)
            return

        if is_number(left):
            if left % 2 == 0 and float(int(log(left, 2))) == log(left, 2):
                count = int(sqrt(left))
                code = """
                LOAD right
                """
                for _ in range(count):
                    code += """
                    SHL
                    """
                code += """
                STORE target
                """
                self.parse(code, right=right, target=target)
                return
            elif left == 1 and target != left:
                code = """
                LOAD right
                STORE target
                """
                self.parse(code, right=right, target=target)
                return
            elif target == right and left == 1:
                return

        code = ""

        if is_number(left) and is_number(right):
            if right > left:
                left, right = right, left

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
            """
        code += """ 
            LOAD left
            SUB right
            JZERO #RIGHT_BIGGER

            #LEFT_BIGGER:
            LOAD left
            STORE r0
            LOAD right
            STORE r1
            JUMP #START
    
            #RIGHT_BIGGER:""" if left != right and not (is_number(left) and is_number(right)) else ''

        code += """
            LOAD right
            STORE r0
            LOAD left
            STORE r1

            #START:
            JZERO #END
            JODD #IS_ODD
            JUMP #NOT_ODD

            #IS_ODD:
            LOAD r2
            ADD r0
            STORE r2

            #NOT_ODD:
            LOAD r0
            SHL
            STORE r0
            
            LOAD r1
            SHR
            STORE r1
            
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
        [left, right] = operands

        if is_number(left) and is_number(right):
            self.parse('GENERATE n', n=0 if right == 0 else left // right)
            self.parse('STORE t', t=target)
            return

        # 0 -> r2
        code = """
               ZERO
               STORE r2
               """
        # x -> r0
        code += """
               GENERATE l_val
               """ if is_number(left) else """
               LOAD left
               """
        code += """
               STORE r0
               JZERO #END
               """
        # y -> r1, r3
        code += """
               GENERATE r_val
               """ if is_number(right) else """
               LOAD right
               """
        code += """
               JZERO #END
               STORE r1
               """
        code += """
               STORE r3
               """ if is_number(right) else ""
        code += """
               JUMP #FIRST_SHIFT
               #SHIFT:
               LOAD r1
               #FIRST_SHIFT:
               SHL
               STORE r1
               SHL
               DEC
               SUB r0
               JZERO #SHIFT
               LOAD r1
               """

        code += """
               #LOOP:
               INC
               SUB {const_addr}
               JZERO #END
               """.format(const_addr='r3' if is_number(right) else 'right')

        code += """
               LOAD r1
               SUB r0
               JZERO #ADD

               #NO_ADD:
               LOAD r2
               SHL
               STORE r2
               LOAD r1
               SHR
               STORE r1
               JUMP #LOOP

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

               #END:
               LOAD {target_reg}
               STORE target
               """.format(target_reg='r2')

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   left=left if is_variable(left) else Reg.r4,
                   right=right if is_variable(right) else Reg.r5,
                   target=target,
                   r0=Reg.r0, r1=Reg.r1, r2=Reg.r2, r3=Reg.r3)

    def operation_modulo(self, target, operands):
        [left, right] = operands

        if is_number(left) and is_number(right):
            self.parse('GENERATE n', n=0 if right == 0 else left % right)
            self.parse('STORE t', t=target)
            return

        code = ''

        # 0 -> r2
        code += """
                       ZERO
                       STORE r2
                       """
        # x -> r0
        code += """
                       GENERATE l_val
                       """ if is_number(left) else """
                       LOAD left
                       """
        code += """
                       STORE r0
                       JZERO #END
                       """
        # y -> r1, r3
        code += """
                       GENERATE r_val
                       """ if is_number(right) else ''
        code += """
                       LOAD right
                """ if not is_number(right) and right != left else ''

        code += """
                       JZERO #END
                       STORE r1
                       """
        code += """
                       STORE r3
                       """ if is_number(right) else ""
        code += """
                       JUMP #FIRST_SHIFT
                       #SHIFT:
                       LOAD r1
                       #FIRST_SHIFT:
                       SHL
                       STORE r1
                       SHL
                       DEC
                       SUB r0
                       JZERO #SHIFT
                       LOAD r1
                       """

        code += """
                       #LOOP:
                       INC
                       SUB {const_addr}
                       JZERO #END
                       """.format(const_addr='r3' if is_number(right) else 'right')

        code += """
                       LOAD r1
                       SUB r0
                       JZERO #ADD

                       #NO_ADD:
                       LOAD r2
                       SHL
                       STORE r2
                       LOAD r1
                       SHR
                       STORE r1
                       JUMP #LOOP

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

                       #END:
                       LOAD {target_reg}
                       STORE target
                       """.format(target_reg='r0')

        self.parse(code,
                   l_val=left,
                   r_val=right,
                   left=left if is_variable(left) else Reg.r4,
                   right=right if is_variable(right) else Reg.r5,
                   target=target,
                   r0=Reg.r0, r1=Reg.r1, r2=Reg.r2, r3=Reg.r3)

    def operation_divmod(self, target, operands, division=True):
        [left, right] = operands

        if is_number(left) and is_number(right):
            if division:
                self.parse('GENERATE n', n=0 if right == 0 else left // right)
            else:
                self.parse('GENERATE n', n=0 if right == 0 else left % right)
            self.parse('STORE t', t=target)
            return

        # TODO: mul two times ?

        # 0 -> r2
        code = """
               ZERO
               STORE r2
               """
        # x -> r0
        code += """
               GENERATE l_val
               """ if is_number(left) else """
               LOAD left
               """
        code += """
               STORE r0
               JZERO #END
               """
        # y -> r1, r3
        code += """
               GENERATE r_val
               """ if is_number(right) else """
               LOAD right
               """
        code += """
               JZERO #END
               STORE r1
               """
        code += """
               STORE r3
               """ if is_number(right) else ""
        code += """
               JUMP #FIRST_SHIFT
               #SHIFT:
               LOAD r1
               #FIRST_SHIFT:
               SHL
               STORE r1
               SHL
               DEC
               SUB r0
               JZERO #SHIFT
               LOAD r1
               """

        code += """
               #LOOP:
               INC
               SUB {const_addr}
               JZERO #END
               """.format(const_addr='r3' if is_number(right) else 'right')

        code += """
               LOAD r1
               SUB r0
               JZERO #ADD

               #NO_ADD:
               LOAD r2
               SHL
               STORE r2
               LOAD r1
               SHR
               STORE r1
               JUMP #LOOP

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

               #END:
               LOAD {target_reg}
               STORE target
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
        source = self.addr_to_reg_if_arr(source, Reg.r10)

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
        target = self.addr_to_reg_if_arr(target, Reg.r10)

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

        if is_number(left) and left == 1:
            code = """
            LOAD a
            JZERO #FALSE
            DEC
            JZERO @label
            #FALSE:
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

        if is_number(left) and left == 0:
            code = """
            LOAD a
            JZERO #FALSE
            JUMP @label
            #FALSE:
            """
            self.parse(code, a=right, label=label)
            return

        if is_number(left) and left == 1:
            code = """
            LOAD a
            JZERO @label
            DEC
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

        if is_number(left) and is_number(right):
            if left > right:
                self.parse('JUMP @label', label=label)
                return

        if is_number(left) and left == 0:
            return

        if is_number(right):
            if right == 0:
                code = """
                JZERO #FALSE
                JUMP @label
                #FALSE:
                """
                self.parse(code, label=label)
                return

        if is_number(right):
            code += """
            GENERATE r_val
            STORE right
            """
        if is_number(left):
            code += """
            GENERATE l_val
            """
        else:
            code += """
            LOAD left
            """
        code += """
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
        if is_number(right):
            code += """
            GENERATE r_val
            STORE right
            """

        if is_number(left):
            code += """
            GENERATE l_val
            """
        else:
            code += """
            LOAD left
            """

        code += """
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
                if is_array(variable):
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
        elif is_reg(index):
            self.code.append(
                '{cmd}I {reg}'.format(cmd=left, reg=index[1])
            )
        elif is_variable(index):
            left += 'I'
            array = self.mem['{}#0'.format(var)]
            arr_start_ptr = array['start_ptr']
            if left == 'LOADI':
                self.code.append('LOAD {arr_start_ptr}'.format(arr_start_ptr=arr_start_ptr))
                code = """
                ADD x
                STORE r9
                LOADI r9
                """
                self.parse(code, x=index, r9=Reg.r9)
            elif left in ['STOREI', 'ADDI', 'SUBI']:
                self.parse("""
                STORE r8
                """, r8=Reg.r8)

                self.code.append('LOAD {arr_start_ptr}'.format(arr_start_ptr=arr_start_ptr))

                code = """ADD x
                STORE r9
                LOAD r8
                {cmd} r9
                """.format(cmd=left, arr_size=arr_start_ptr)
                self.parse(code, x=index, r9=Reg.r9, r8=Reg.r8)
            else:
                raise CompilerError("Unexpected command")

    def end(self):
        self.parse('HALT')
