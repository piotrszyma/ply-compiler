from lib.error import CompilerError


class Optimization:
    __slots__ = {
        'cmds',
        'labels'
    }

    def __init__(self):
        self.cmds = []

    def optimize(self, cmds):
        self.cmds = cmds
        self.opt_remove_store_load()
        self.opt_halt_if_no_write()
        self.opt_jump_to_load_after_store()
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
            self.cmds = ['GET'] * reads if reads > 0 else [] + ['HALT']

    def opt_jump_to_load_after_store(self):
        cmds = self.cmds
        labels = {}
        indexes = {}
        jumps = {}
        for (lineno, c) in enumerate(cmds):
            if isinstance(c, tuple):
                if c[0] == 'label':
                    if c[1] in labels.keys():
                        raise CompilerError("Labels duplication")
                    else:
                        labels[c[1]] = self.get_label_successor(lineno)
                        indexes[c[1]] = lineno
                elif c[0] in ['JUMP', 'JZERO']:
                    if c[1] not in jumps.keys():
                        jumps[c[1]] = {self.get_jump_predecessor(lineno)}
                    else:
                        jumps[c[1]] = {*jumps[c[1]], self.get_jump_predecessor(lineno)}
        jumps = dict(map(lambda j: (j[0], *j[1]), filter(lambda j: len(j[1]) == 1, jumps.items())))
        # for label, cmd in labels.items():
        #     if cmd is None:
        #         continue
        #     if isinstance(cmd, tuple):
        #         continue
        #     label_cmd, l_addr, *_ = cmd.split(' ') + [' ']
        #     pre_jump = jumps.get(label, None)
        #     if pre_jump is None:
        #         continue
        #     pre_jump_cmd, p_addr, *_ = pre_jump.split(' ') + [' ']
        #     if l_addr == p_addr and label_cmd == 'LOAD' and pre_jump_cmd == 'STORE':
        #         i = indexes[label]
        #         self.cmds[i], self.cmds[i - 1] = self.cmds[i - 1], self.cmds[i]

    def get_label_successor(self, label_index):
        if label_index == len(self.cmds) - 1:
            return None
        else:
            return self.cmds[label_index + 1]

    def get_jump_predecessor(self, jump_index):
        if jump_index == 0:
            return self.cmds[jump_index]
        elif isinstance(self.cmds[jump_index - 1], tuple):
            return self.get_jump_predecessor(jump_index - 1)
        else:
            return self.cmds[jump_index - 1]
