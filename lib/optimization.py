class Optimization:
    __slots__ = {
        'cmds'
    }

    def __init__(self):
        self.cmds = []

    def optimize(self, cmds):
        self.cmds = cmds
        self.opt_remove_store_load()
        self.opt_halt_if_no_write()
        return self.cmds

    def opt_remove_store_load(self):
        """
        STORE x
        LOAD x

         \/

        STORE x
        """
        cmds = self.cmds

        for index, cmd in enumerate(cmds[:-1]):
            u_i = index
            l_i = index + 1

            if isinstance(cmds[u_i], str) and isinstance(cmds[l_i], str):
                u_cmd, u_addr = (cmds[u_i].split(' ') + [''])[:2]
                l_cmd, l_addr = (cmds[l_i].split(' ') + [''])[:2]

                if u_cmd == 'STORE' and l_cmd == 'LOAD' and u_addr == l_addr:
                    cmds[l_i] = 'DELETE'

        self.cmds = list(filter(lambda x: x != 'DELETE', cmds))

    def opt_halt_if_no_write(self):
        reads = self.cmds.count('GET')
        writes = self.cmds.count('PUT')
        if writes == 0:
            self.cmds = ['GET' * reads] if reads > 0 else [] + ['HALT']
