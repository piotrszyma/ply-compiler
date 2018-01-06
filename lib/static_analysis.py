import logging

from lib.error import CompilerError
from lib.utils import is_variable, raise_error, is_int, is_array, is_operation, is_expression, is_number


class StaticAnalyzer:
    __slots__ = {
        'scope',
        'symbols',
        'initialized',
        'iterators',
        'arrays'
    }

    def __init__(self):
        self.symbols = set()
        self.scope = set()
        self.initialized = {}
        self.iterators = set()
        self.arrays = {}

    def add_iterator(self, var):
        self.iterators.add(var)
        self.symbols.add(var)
        # symbol with # means counter for loop
        self.symbols.add('#' + var)
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

        parsed_symbols = [s[:-2] + '#' + str(self.arrays[s]) if s[-2:] == '#0' else s for s in self.symbols]

        return parsed_symbols, commands

    def check_for_duplicate_declarations(self, declarations):
        seen = []
        arrays = {}

        for kind, val, *details, lineno in declarations:
            if val in seen:
                raise_error(
                    msg='double declaration of {}'.format(val),
                    lineno=lineno
                )
            if kind == 'int[]':
                [size] = details
                seen.append(val + '#0')
                if val in arrays.keys():
                    raise_error(
                        msg='double declaration of array {}'.format(val),
                        lineno=lineno
                    )
                arrays[val + '#0'] = size
            else:
                seen.append(val)
        self.symbols = set(seen)
        self.scope = set(seen)
        self.arrays = arrays

    def check_commands(self, cmds):
        for c in cmds:
            getattr(self, 'check_{type}'.format(type=c[0]))(c)

    def check_assign(self, cmd):
        _, target, expression = cmd
        self.check_scope(target)

        if is_int(target):
            _, symbol, lineno = target
            if symbol in self.iterators:
                raise_error("Mutation of iterator '{symbol}'".format(symbol=symbol), lineno)
        elif is_array(target):
            _, symbol, index, _ = target
            symbol = '#'.join([symbol, str(index)])
        else:
            raise CompilerError("Unexpected target type")

        self.check_expression(expression)
        self.initialized[symbol] = True

    def check_expression(self, cmd):
        _, *expression = cmd
        if len(expression) == 1:
            [var] = expression
            if is_variable(var):
                self.check_variable(var)
                self.check_initialized(var)
        elif len(expression) == 3:
            [_, l_var, r_var] = expression
            for var in [l_var, r_var]:
                if is_variable(var):
                    self.check_variable(var)
                    self.check_initialized(var)
        else:
            raise CompilerError("Unexpected expression")

    def check_initialized(self, var):
        if is_int(var):
            _, symbol, lineno = var
            if not self.initialized.get(symbol, False):
                raise_error("Usage of uninitialized variable '{symbol}'".format(symbol=symbol), lineno)
        elif is_array(var):
            # Cannot check int tab initialization
            pass

    def check_write(self, cmd):
        _, operand = cmd
        if is_variable(operand):
            self.check_variable(operand)
            self.check_initialized(operand)

    def check_read(self, cmd):
        _, operand = cmd
        self.check_variable(operand)
        _, symbol, *_ = operand
        self.initialized[symbol] = True

    def check_if_then(self, cmd):
        _, condition, cmds = cmd
        self.check_condition(condition)
        self.check_commands(cmds)

    def check_if_else(self, cmd):
        _, condition, true_cmds, false_cmds = cmd
        self.check_condition(condition)
        for cmds in [true_cmds, false_cmds]:
            self.check_commands(cmds)

    def check_while(self, cmd):
        _, condition, cmds = cmd
        self.check_condition(condition)
        self.check_commands(cmds)

    def check_condition(self, condition):
        *_, left_op, right_op = condition
        for operand in [left_op, right_op]:
            if is_variable(operand):
                self.check_variable(operand)
                self.check_initialized(operand)

    def check_for_up(self, cmd):
        _, iterator, start, end, cmds = cmd

        for el in [v for v in [start, end] if is_variable(v)]:
            if is_variable(el):
                self.check_variable(el)
                self.check_initialized(el)

        self.check_iterator(iterator)
        _, iter_symbol, iter_lineno = iterator

        self.add_iterator(iter_symbol)
        self.initialized[iter_symbol] = True

        self.analyze(cmds)

        self.initialized[iter_symbol] = False
        self.remove_from_scope(iter_symbol)

    def check_for_down(self, cmd):
        self.check_for_up(cmd)

    def check_iterator(self, iterator):
        _, iter_symbol, iter_lineno = iterator
        if iter_symbol in self.scope:
            raise_error(
                msg="trying to set previously declared variable '{0}' as iterator".format(iter_symbol),
                lineno=iter_lineno
            )
            raise CompilerError()

    def check_variable(self, variable):
        if is_int(variable):
            self.check_int(variable)
        elif is_array(variable):
            self.check_inttab(variable)
        else:
            raise CompilerError("Unexpected variable type")

    def check_inttab(self, variable):
        _, symbol, index, lineno = variable

        arr_start = '#'.join([symbol, '0'])

        if arr_start not in self.scope:
            raise_error("Usage of undeclared array {}".format(symbol), lineno)
        if is_number(index):
            self.check_inttab_index(variable)
        elif is_int(index):
            self.check_variable(index)
        else:
            raise CompilerError("Unexpected array index")

    def check_inttab_index(self, variable):
        _, symbol, index, lineno = variable
        if not 0 <= index <= self.arrays[symbol + '#0'] - 1:
            raise_error("Array {} index out of range".format(symbol), lineno)

    def check_int(self, variable):
        _, symbol, lineno = variable
        if '#'.join([symbol, '0']) in self.scope:
            raise_error(
                msg="Usage of array variable '{symbol}' without specifing index".format(symbol=symbol),
                lineno=lineno
            )
        if symbol not in self.scope:
            raise_error(
                msg="Variable '{symbol}' not declared".format(symbol=symbol),
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
        elif is_array(operand):
            if is_number(operand[2]):
                self.check_inttab(operand)
        else:
            raise CompilerError("Unexpected operand")
