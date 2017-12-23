import logging

from lib.error import CompilerError
from lib.utils import is_variable, raise_error


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
        # TODO: check other commands, add locals
        # returns list of variables & commands
        return self.symbols, commands

    def check_for_duplicate_declarations(self, declarations):
        seen = []
        for kind, val, *details, lineno in declarations:
            if val in seen:
                logging.error(' In line {}: double declaration of {}'.format(
                    lineno,
                    val))
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
        for op in cmd[1:]:
            if is_variable(op):
                if op[1] not in self.scope:
                    import pdb;
                    pdb.set_trace()

    def check_expression(self, cmd):
        if cmd[1][1] not in self.scope:
            raise_error(
                msg="undeclared variable {0} ".format(cmd[1][1]),
                lineno=cmd[1][2]
            )

    def check_write(self, cmd):
        _, operand = cmd
        if is_variable(operand):
            name = operand[1]
            lineno = operand[-1]
            if name not in self.scope:
                raise_error(
                    msg="undeclared variable {0} ".format(name),
                    lineno=lineno
                )

    def check_if_then(self, cmd):
        pass

    def check_for_up(self, cmd):
        _, iterator, start, end, cmds = cmd
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
        self.add_to_symbols('#' + iterator[1])
