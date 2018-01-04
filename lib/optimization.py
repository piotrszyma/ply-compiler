class Optimization:
    def optimize(self, cmds):
        cmds = self.opt_remove_store_load(cmds)
        return cmds

    def opt_remove_store_load(self, cmds):
        """
        STORE x
        LOAD x

         \/

        STORE x
        """

        for index, cmd in enumerate(cmds[:-1]):
            u_i = index
            l_i = index + 1

            if isinstance(cmds[u_i], str) and isinstance(cmds[l_i], str):
                u_cmd, u_addr = (cmds[u_i].split(' ') + [''])[:2]
                l_cmd, l_addr = (cmds[l_i].split(' ') + [''])[:2]

                if u_cmd == 'STORE' and l_cmd == 'LOAD' and u_addr == l_addr:
                    cmds[l_i] = 'DELETE'

        cmds = filter(lambda x: x != 'DELETE', cmds)

        return cmds
