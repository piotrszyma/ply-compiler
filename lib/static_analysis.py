import logging

from lib.error import CompilerError


class StaticAnalyzer:
    __slots__ = {
        'globals',
        'locals'
    }

    def __init__(self):
        self.globals = []

    def analyze(self, parse_tree):
        _, declarations, commands = parse_tree

        self.check_for_duplicate_declarations(declarations)
        self.check_commands(commands)

    def check_for_duplicate_declarations(self, declarations):
        seen = []
        for (_, declaration, lineno) in declarations:
            if declaration in seen:
                logging.error(' In line {}: double declaration of {}'.format(lineno, declaration))
                raise CompilerError()
            seen.append(declaration)

        self.globals = seen

    def check_commands(self, commands):
        # TODO: commands check
        pass
