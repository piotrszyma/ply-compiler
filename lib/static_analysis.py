import logging

from lib.error import CompilerError
from lib.utils import is_variable, raise_error, is_int, is_inttab, is_operation, is_expression, is_number


class StaticAnalyzer:
    __slots__ = {
        'scope',
        'symbols'
    }

    def __init__(self):
        self.symbols = set()
        self.scope = set()

    def add_to_scope(self, var):
        self.symbols.add(var)
        self.scope.add(var)

    def remove_from_scope(self, var):
        self.scope.remove(var)

    def add_to_symbols(self, var):
        self.symbols.add(var)

    def analyze(self, parse_tree):
        if parse_tree[0] == 'program':
            _, declarations, commands = parse_tree
            self.check_for_duplicate_declarations(declarations)
        else:
            commands = parse_tree
        self.check_commands(commands)
        return self.symbols, commands

    def check_for_duplicate_declarations(self, declarations):
        seen = []
        for kind, val, *details, lineno in declarations:
            if val in seen:
                raise_error(
                    msg='double declaration of {}'.format(val),
                    lineno=lineno
                )
                raise CompilerError()
            if kind == 'int[]':
                [size] = details
                seen.extend([val + '#' + str(i) for i in range(size)])
            else:
                seen.append(val)
        self.symbols = self.scope = {*seen}

    def check_commands(self, cmd):
        for c in cmd:
            getattr(self, 'check_{type}'.format(type=c[0]))(c)
            # TODO: commands check

    def check_assign(self, cmd):
        _, left, right = cmd
        self.check_scope(left)
        self.check_scope(right)

    def check_expression(self, cmd):
        if cmd[1][1] not in self.scope:
            raise_error(
                msg="undeclared variable {0} ".format(cmd[1][1]),
                lineno=cmd[1][2]
            )

    def check_write(self, cmd):
        _, operand = cmd
        if is_variable(operand):
            self.check_scope(operand)

    def check_read(self, cmd):
        _, operand = cmd
        if is_variable(operand):
            self.check_scope(operand)

    def check_if_then(self, cmd):
        pass

    def check_if_else(self, cmd):
        pass

    def check_while(self, cmd):
        pass

    def check_for_up(self, cmd):
        _, iterator, start, end, cmds = cmd
        # TODO: check if iterator is not array, number
        if iterator in self.symbols:
            raise_error(
                msg="trying to set previously declared variable '{0}' as iterator".format(iterator[1]),
                lineno=iterator[2]
            )
            raise CompilerError()
        self.add_to_scope(iterator[1])
        self.analyze(cmds)
        self.remove_from_scope(iterator[1])
        # with # means -> counter for this loop
        self.add_to_symbols(iterator[1])
        self.add_to_symbols('#' + iterator[1])

    def check_for_down(self, cmd):
        # TODO: check if iterator is not array, number
        _, iterator, start, end, cmds = cmd
        # TODO: check if iterator is not array, number
        if iterator in self.symbols:
            raise_error(
                msg="trying to set previously declared variable '{0}' as iterator".format(iterator[1]),
                lineno=iterator[2]
            )
            raise CompilerError()
        self.add_to_scope(iterator[1])
        self.analyze(cmds)
        self.remove_from_scope(iterator[1])
        # with # means -> counter for this loop
        self.add_to_symbols(iterator[1])
        self.add_to_symbols('#' + iterator[1])

    def check_scope(self, operand):
        if is_number(operand):
            pass
        elif is_int(operand):
            if operand[1] not in self.scope:
                raise_error(
                    msg="Undeclared variable {}".format(operand[1]),
                    lineno=operand[2]
                )
        elif is_inttab(operand):
            name = '{arr_name}#{index}'.format(
                arr_name=operand[1],
                index=operand[2]
            )
            if name not in self.scope:
                raise_error(
                    msg="Undeclared variable {}".format(operand[1])
                )
        elif is_operation(operand):
            import pdb;
            pdb.set_trace()
        elif is_expression(operand):
            if len(operand) == 4:
                self.check_scope(operand[2])
                self.check_scope(operand[3])
            elif len(operand) == 2:
                self.check_scope(operand[1])
            else:
                raise CompilerError("Unexpected operand")

        else:
            raise CompilerError("Unexpected operand")
