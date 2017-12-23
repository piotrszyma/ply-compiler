def is_number(a):
    return isinstance(a, int)


def is_int(a):
    return isinstance(a, tuple) and \
           len(a) == 3 and \
           a[0] == 'int'


def is_operation(a):
    return isinstance(a, list) and \
           len(a) == 3


def is_inttab(a):
    return isinstance(a, tuple) \
           and len(a) == 3 \
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


def get_symbol(a):
    if is_int(a):
        return a[1]
    elif is_inttab(a):
        return str(a[1]) + '#' + str(a[2])
    elif is_swap(a):
        return a
