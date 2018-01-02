import logging

from lib.error import CompilerError
from lib.utils import is_variable, raise_error, is_int, is_inttab, is_operation, is_expression, is_number


class StaticAnalyzer:
    __slots__ = {
        'scope',
        'symbols',
        'initialized'
    }

    def __init__(self):
        self.symbols = set()
        self.scope = set()
        self.initialized = {}

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
        _, target, expression = cmd
        self.check_scope(target)
        self.check_expression(expression)
        if is_int(target):
            _, symbol, _ = target
        elif is_inttab(target):
            _, symbol, index, _ = target
            symbol = '#'.join([symbol, str(index)])
        else:
            raise CompilerError("Unexpected target type")
        self.initialized[symbol] = True

    def check_expression(self, cmd):
        _, *expression = cmd
        if len(expression) == 1:
            [var] = expression
            if is_variable(var):
                self.check_variable(var)
                self.check_if_initialized(var)
        elif len(expression) == 3:
            [_, l_var, r_var] = expression
            for var in [l_var, r_var]:
                if is_variable(var):
                    self.check_variable(var)
                    self.check_if_initialized(var)
        else:
            raise CompilerError("Unexpected expression")

    def check_if_initialized(self, var):
        if is_int(var):
            _, symbol, lineno = var
            if not self.initialized.get(symbol, False):
                raise_error("Usage of uninitialized variable '{symbol}'".format(symbol=symbol), lineno)
        elif is_inttab(var):
            _, symbol, index, lineno = var
            if not is_number(index):
                return
            symbol = '#'.join([symbol, str(index)])
            if not self.initialized.get(symbol, False):
                raise_error("Usage of uninitialized array element '{symbol}'".format(symbol=symbol), lineno)

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
        _, (_, iter_symbol, iter_lineno), start, end, cmds = cmd
        # TODO: check if iterator is not array, number
        if iter_symbol in self.symbols:
            raise_error(
                msg="trying to set previously declared variable '{0}' as iterator".format(iter_symbol),
                lineno=iter_lineno
            )
            raise CompilerError()
        self.add_to_scope(iter_symbol)
        self.analyze(cmds)
        self.remove_from_scope(iter_symbol)
        # symbol with # means counter for loop
        self.add_to_symbols(iter_symbol)
        self.add_to_symbols('#' + iter_symbol)

    def check_for_down(self, cmd):
        # TODO: check if iterator is not array, number
        _, (_, iter_symbol, iter_lineno), start, end, cmds = cmd
        # TODO: check if iterator is not array, number
        if iter_symbol in self.symbols:
            raise_error(
                msg="trying to set previously declared variable '{0}' as iterator".format(iter_symbol),
                lineno=iter_lineno
            )
            raise CompilerError()
        self.add_to_scope(iter_symbol)
        self.analyze(cmds)
        self.remove_from_scope(iter_symbol)
        # with # means counter for this loop
        self.add_to_symbols(iter_symbol)
        self.add_to_symbols('#' + iter_symbol)

    def check_variable(self, variable):
        if is_int(variable):
            self.check_int(variable)
        elif is_inttab(variable):
            self.check_inttab(variable)
        else:
            import pdb; pdb.set_trace()
            raise CompilerError("Unexpected variable type")

    def check_inttab(self, variable):
        _, symbol, index, lineno = variable

        arr_start = '#'.join([symbol, '0'])

        if arr_start not in self.scope:
            raise_error("Usage of undeclared array {}".format(symbol), lineno)

        if is_number(index):
            el_symbol = '#'.join([symbol, str(index)])
            if el_symbol not in self.scope:
                raise_error("Array index out of scope".format(symbol), lineno)
        elif is_int(index):
            self.check_variable(index)
        else:
            raise CompilerError("Unexpected array index")

    def check_int(self, variable):
        _, symbol, lineno = variable
        if '#'.join([symbol, '0']) in self.scope:
            raise_error(
                msg="Usage of array variable '{symbol}' without specifing index".format(symbol=symbol),
                lineno=lineno
            )
        if symbol not in self.scope:
            raise_error(
                msg='Variable {symbol} not initialized'.format(symbol=symbol),
                lineno=lineno
            )

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
            if is_number(operand[2]):
                arr_start = '{arr_name}#{index}'.format(
                    arr_name=operand[1],
                    index=0
                )
                name = '{arr_name}#{index}'.format(
                    arr_name=operand[1],
                    index=operand[2]
                )
                if arr_start not in self.scope:
                    if operand[1] in self.scope:
                        raise_error("Trying to assign to array '{}' without specifing index".format(operand[1]))
                    raise_error("Undeclared array {}".format(operand[1]))
                if name not in self.scope:
                    raise_error(
                        msg="Array index out of range {}".format(operand[1])
                    )
        else:
            raise CompilerError("Unexpected operand")

