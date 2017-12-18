from lib.machine import Machine


class CodeGenerator:
    __slots__ = {
        'memtab',
        'reg',
        'machine'
    }

    def __init__(self):
        self.memtab = {}
        self.reg = None
        self.machine = Machine()

    def generate(self, flow_graph, symtab):

        self.machine.reserve_memory(symtab)

        for cmd in flow_graph[0]:
            getattr(self, 'gen_' + cmd[0])(cmd)

        self.machine.end()

        return '\n'.join(self.machine.code) + '\n'

    def gen_assign(self, cmd):
        _, variable, expression = cmd
        self.machine.assign(variable, expression)

    def gen_write(self, cmd):
        _, variable = cmd
        self.machine.write(variable)
