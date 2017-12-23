from lib.machine import Machine


class CodeGenerator:
    __slots__ = {
        'memtab',
        'reg',
        'machine'
    }

    def __init__(self):
        self.memtab = {}
        self.machine = Machine()

    def generate(self, flow_graph, symtab):
        self.machine.reserve_memory(symtab)
        self.machine.set_labels(flow_graph)
        for cmd in flow_graph:
            getattr(self, 'gen_' + cmd[0])(cmd)

        self.machine.resolve_labels()
        self.machine.end()
        return '\n'.join(self.machine.code) + '\n'

    def gen_assign(self, cmd):
        _, variable, expression = cmd
        self.machine.assign(variable, expression)

    def gen_write(self, cmd):
        _, variable = cmd
        self.machine.write(variable)

    def gen_read(self, cmd):
        _, variable = cmd
        self.machine.read(variable)

    def gen_if(self, cmd):
        self.machine.check_if(cmd)

    def gen_label(self, cmd):
        self.machine.code.append(cmd,)

    def gen_goto(self, cmd):
        self.machine.code += ('JUMP', cmd[1]),
