import logging

from lib.error import CompilerError


def is_number(a):
    return isinstance(a, int)


def is_int(a):
    return isinstance(a, tuple) and \
           len(a) == 3 and \
           a[0] == 'int'


def is_operation(a):
    return isinstance(a, list) and \
           len(a) == 3


def is_expression(a):
    return a[0] == 'expression' and \
           (len(a) == 2 or len(a) == 4)


def is_inttab(a):
    return isinstance(a, tuple) \
           and len(a) == 4 \
           and a[0] == 'int[]'


def is_variable(a):
    return is_int(a) or is_inttab(a)


def is_swap(a):
    return isinstance(a, int) \
           and 0 <= a <= 9


def is_label(a):
    return isinstance(a, tuple) \
           and len(a) == 2 \
           and a[0] == 'label'


def raise_error(msg, lineno=None):
    error_msg = ""
    if lineno:
        error_msg += " in line {0}: ".format(lineno)
    error_msg += msg
    logging.error(error_msg)
    raise CompilerError()


def arr_sort(element):
    hash_index = element.find('#')
    arr_name = element[:hash_index]
    arr_index = int(element[hash_index + 1:])
    return arr_name, arr_index


def symtab_sort(symtab):
    var_addr = list(filter(lambda x: '#' not in x, symtab))
    arr_addr = sorted(list(filter(lambda x: '#' in x[1:], symtab)), key=arr_sort)
    iter_addr = list(filter(lambda x: x[0] == '#', symtab))
    return var_addr + arr_addr + iter_addr
