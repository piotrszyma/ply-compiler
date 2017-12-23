import logging

from lib.error import CompilerError
from lib.utils import is_variable


class StaticAnalyzer:
    __slots__ = {
        'globals',
        'locals',
        'all_locals'
    }

    def __init__(self):
        self.globals = []
        self.locals = []
        self.all_locals = set()

    def add_local(self, local):
        self.all_locals.add(local)
        self.locals.append(local)

    def remove_local(self, local):
        self.locals.remove(local)

    def analyze(self, parse_tree):
        _, declarations, commands = parse_tree

        self.check_for_duplicate_declarations(declarations)
        self.check_commands(commands)

        # TODO: check other commands, add locals

        # returns list of variables & commands
        return (self.globals + list(self.all_locals)), commands

    def check_for_duplicate_declarations(self, declarations):
        seen = []
        for type, val, *details, lineno in declarations:
            if val in seen:
                logging.error(' In line {}: double declaration of {}'.format(
                    lineno,
                    val))
                raise CompilerError()
            if type == 'int[]':
                [size] = details
                seen.extend([val + '#' + str(i) for i in range(size)])
            else:
                seen.append(val)

        self.globals = seen

    def check_commands(self, cmd):
        for c in cmd:
            getattr(self, 'check_{type}'.format(type=c[0]))(c)
        # TODO: commands check

    def check_assign(self, cmd):
        for op in cmd[1:]:
            if is_variable(op):
                if op not in self.globals:
                    import pdb; pdb.set_trace()

        import pdb; pdb.set_trace()

    def check_expression(self, cmd):
        import pdb; pdb.set_trace()

    def check_for_up(self, cmd):
        _, iterator, start, end, cmds = cmd
        if iterator in self.globals:
            logging.error(" in line {lineno}: trying to set previously declared variable '{value}' as iterator".format(
                lineno=iterator[2],
                value=iterator[1]
            ))
            raise CompilerError()

        iterator = (iterator[0], '#' + iterator[1], iterator[2])
        self.add_local('#' + iterator[1])
        # TODO: locals of loop
