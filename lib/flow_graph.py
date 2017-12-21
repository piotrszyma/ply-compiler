class FlowGraph:
    __slots__ = {
        'flow',
        'label'
    }

    def __init__(self):
        self.flow = [[]]
        self.label = 0

    def generate(self, ast):
        for c in ast:
            getattr(self, 'flow_' + c[0])(c)

        return self.flow

    def next_label(self):
        # TODO: refactor to generator of (1, 2, 3, ...)
        self.label += 1
        return self.label

    def flow_assign(self, cmd):
        self.flow[-1].append(cmd)

    def flow_write(self, cmd):
        self.flow[-1].append(cmd)

    def flow_if_then(self, cmd):
        _, cond, if_true = cmd
        label_t, label_f = self.next_label()
         # = self.next_label()
        # TODO: finish
        cmd = [('if', self.neg(cond))]
        cmd += [('')]
        import pdb; pdb.set_trace()

    def flow_if_else(self, cmd):
        _, cond, if_true, if_false = cmd
        import pdb; pdb.set_trace()

    def neg(self, cond):
        lside, op, rside = cond
        neg_map = {
            '=': lambda l, r: (l, '<>', r),
            '<>': lambda l, r: (l, '=', r),
            '>=': lambda l, r: (l, '<', r),
            '>': lambda l, r: (l, '<=', r),
            '<=': lambda l, r: (l, '>', r),
            '<': lambda l, r: (l, '>=', r)
        }
        return neg_map[op](lside, rside)

    def norm(self, cond):
        lside, op, rside = cond
        norm_map = {
            '=': lambda l, r: (l, '=', r),
            '<>': lambda l, r: (l, '<>', r),
            '>=': lambda l, r: (l, '>=', r),
            '>': lambda l, r: (l, '>', r),
            '<=': lambda l, r: (r, '>=', l),
            '<': lambda l, r: (r, '>', l)
        }
        return norm_map[op](lside, rside)
