class FlowGraph:
    __slots__ = {
        'flow'
    }

    def __init__(self):
        self.flow = [[]]

    def generate(self, ast):
        # TODO: parse WHILE, FOR UP, FOR DOWN, IFs
        for c in ast:
            getattr(self, 'flow_' + c[0])(c)

        return self.flow

    def flow_assign(self, cmd):
        self.flow[-1].append(cmd)

    def flow_write(self, cmd):
        self.flow[-1].append(cmd)

