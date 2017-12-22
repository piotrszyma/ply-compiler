class FlowGraph:
    __slots__ = {
        'flow',
        'label'
    }

    def __init__(self):
        self.flow = []
        self.label = 0

    def generate(self, ast, main=False):
        for c in ast:
            getattr(self, 'flow_' + c[0])(c)

        if main:
            return self.flow

    def next_label(self):
        # TODO: refactor to generator of (1, 2, 3, ...)
        self.label += 1
        return 'label{0}'.format(self.label)

    def flow_assign(self, cmd):
        self.flow.append(cmd)

    def flow_write(self, cmd):
        self.flow.append(cmd)

    def flow_if_then(self, cmd):
        _, cond, if_true = cmd
        label_false = self.next_label()
        self.flow += self.add_goto_if(self.neg(cond), label_false)
        self.generate(if_true)
        self.flow += ('label', label_false),

    def flow_if_else(self, cmd):
        _, cond, if_true, if_false = cmd
        label_false, label_end = self.next_label(), self.next_label()
        self.flow += self.add_goto_if(self.neg(cond), label_false)
        self.generate(if_true)
        self.flow += self.add_goto(label_end)
        self.flow += ('label', label_false),
        self.generate(if_false)
        self.flow += self.add_label(label_end)

    def neg(self, cond):
        op, lside, rside = cond[1:]
        neg_map = {
            '=':  lambda l, r: (l, '<>', r),
            '<>': lambda l, r: (l, '=', r),
            '>=': lambda l, r: (l, '<', r),
            '>':  lambda l, r: (l, '<=', r),
            '<=': lambda l, r: (l, '>', r),
            '<':  lambda l, r: (l, '>=', r)
        }
        return neg_map[op](lside, rside)

    def norm(self, cond):
        lside, op, rside = cond
        norm_map = {
            '=':  lambda l, r: (l, '=', r),
            '<>': lambda l, r: (l, '<>', r),
            '>=': lambda l, r: (l, '>=', r),
            '>':  lambda l, r: (l, '>', r),
            '<=': lambda l, r: (r, '>=', l),
            '<':  lambda l, r: (r, '>', l)
        }
        return norm_map[op](lside, rside)

    def add_goto_if(self, cond, label):
        return ('if', cond, 'goto', label),

    def add_goto(self, label):
        return ('goto', label),

    def add_label(self, label):
        return ('label', label),
