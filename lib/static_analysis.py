import logging

from lib.error import CompilerError


class StaticAnalyzer:
    __slots__ = {
        'globals'
    }

    def __init__(self):
        self.globals = []

    def analyze(self, parse_tree):
        _, declarations, commands = parse_tree

        self.check_for_duplicate_declarations(declarations)
        self.check_commands(commands)

        # TODO: check other commands, add locals

        # returns list of variables & commands
        return self.globals, commands

    def check_for_duplicate_declarations(self, declarations):
        seen = []
        for _, val, *_, lineno in declarations:
            if val in seen:
                logging.error(' In line {}: double declaration of {}'.format(
                    lineno,
                    val))
                raise CompilerError()
            seen.append(val)

        self.globals = seen

    def check_commands(self, commands):
        # TODO: commands check
        pass
