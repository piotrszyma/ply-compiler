class FlowGraph:
    __slots__ = {
        'flow',
        'label'
    }

    def __init__(self):
        self.flow = []
        self.label = 0

    def generate(self, ast):
        for c in ast:
            getattr(self, 'flow_' + c[0])(c)
        return self.flow

    def next_label(self, multiple=1):
        # TODO: refactor to generator of (1, 2, 3, ...)
        labels = tuple('label' + str(n) for n in range(self.label,
                                                       self.label + multiple))
        self.label += len(labels)
        return labels if multiple != 1 else labels[0]

    def flow_assign(self, cmd):
        self.flow.append(cmd)

    def flow_write(self, cmd):
        self.flow.append(cmd)

    def flow_read(self, cmd):
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

    def flow_while(self, cmd):
        _, cond, body = cmd
        label_start, label_end = self.next_label(2)
        self.flow += self.add_label(label_start)
        self.flow += self.add_goto_if(self.neg(cond), label_end)
        self.generate(body)
        self.flow += self.add_goto(label_start)
        self.flow += self.add_label(label_end)

    def flow_for_up(self, cmd):
        _, iterator, start, end, body = cmd
        counter = (iterator[0], '#' + iterator[1], iterator[2])
        label_start, label_end = self.next_label(2)

        # self.flow += self.add_goto_if((start, '>', end), label_end)

        self.flow += ('assign', counter, ('expression', '-', end, start)),
        self.flow += self.add_goto_if((counter, '=', 0), label_end)
        self.flow += ('assign', counter, ('expression', '+', counter, 1)),
        self.flow += ('assign', iterator, ('expression', start)),

        self.flow += self.add_label(label_start)
        self.flow += self.add_goto_if((counter, '=', 0), label_end)

        self.generate(body)

        self.flow += ('assign', counter, ('expression', '-', counter, 1)),
        self.flow += ('assign', iterator, ('expression', '+', iterator, 1)),
        self.flow += self.add_goto(label_start)
        self.flow += self.add_label(label_end)

    def flow_for_down(self, cmd):
        _, iterator, start, end, body = cmd
        counter = (iterator[0], '#' + iterator[1], iterator[2])

        label_start, label_end = self.next_label(2)

        # self.flow += self.add_goto_if((start, '<', end), label_end)

        self.flow += ('assign', counter, ('expression', '-', start, end)),
        self.flow += self.add_goto_if((counter, '=', 0), label_end)
        self.flow += ('assign', counter, ('expression', '+', counter, 1)),
        self.flow += ('assign', iterator, ('expression', start)),

        self.flow += self.add_label(label_start)
        self.flow += self.add_goto_if((counter, '=', 0), label_end)

        self.generate(body)

        self.flow += ('assign', counter, ('expression', '-', counter, 1)),
        self.flow += ('assign', iterator, ('expression', '-', iterator, 1)),
        self.flow += self.add_goto(label_start)
        self.flow += self.add_label(label_end)

    def add_goto_if(self, cond, label):
        return ('if', cond, 'goto', label),

    def add_goto(self, label):
        return ('goto', label),

    def add_label(self, label):
        return ('label', label),

    def add_expression(self, symbol, left, right):
        return 'expression', symbol, left, right

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
