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

        pre = 1
        post = 0
        while pre != post:
            pre = len(self.cmds)
            self.opt_load_store_load_store_redundancy()
            post = len(self.cmds)

        pre = 1
        post = 0

        while pre != post:
            pre = len(self.cmds)
            self.opt_zero_store_zero_store_redundancy()
            post = len(self.cmds)

        self.opt_jump_after_label()

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
                    cmds[l_i] = 'REMOVE'

        self.cmds = list(filter(lambda x: x != 'REMOVE', cmds))

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

        for label, cmd in [(k, v) for k, v in labels.items() if
                           (v is not None and isinstance(v, str) and v.split(' ')[0] == 'LOAD')]:

            if label not in jumps.keys() or not isinstance(jumps[label], str):
                continue

            if jumps[label].split(' ')[0] == 'STORE':
                _, load_addr = cmd.split(' ')
                _, store_addr = jumps[label].split(' ')
                if load_addr == store_addr:
                    adr = indexes[label]
                    cmds[adr], cmds[adr + 1] = cmds[adr + 1], cmds[adr]
        self.cmds = cmds

    def opt_load_store_load_store_redundancy(self):
        cmds = self.cmds

        index = 0
        max = len(self.cmds)
        while index < max - 3:
            if cmds[index] == cmds[index + 2] and cmds[index][:4] == 'LOAD' and cmds[index + 1][:5] == 'STORE':
                cmds[index + 2] = 'REMOVE'
                index += 3
            else:
                index += 1
        cmds = list(filter(lambda x: x != 'REMOVE', cmds))

        self.cmds = cmds

    def opt_zero_store_zero_store_redundancy(self):
        cmds = self.cmds

        index = 0
        max = len(self.cmds)

        while index < max - 3:
            if cmds[index] == 'ZERO' and \
                            cmds[index + 2] == 'ZERO' and \
                                    cmds[index + 1][:5] == cmds[index + 3][:5] == 'STORE':
                cmds[index + 2] = 'REMOVE'
                index += 4
            else:
                index += 1
        cmds = list(filter(lambda x: x != 'REMOVE', cmds))

        self.cmds = cmds

    def opt_jump_after_label(self):
        """
        ('label', 'label1')
            ...
        ('label', 'label2')
        ('JUMP', 'label1')
        """
        cmds = self.cmds

        index = 0
        max = len(self.cmds)

        while index < max - 1:
            if isinstance(cmds[index], tuple) and isinstance(cmds[index + 1], tuple):
                if cmds[index][0] == 'label' and cmds[index + 1][0] == 'JUMP':
                    to_replace = cmds[index][1]
                    replaced_by = cmds[index + 1][1]
                    cmds[index] = 'REMOVE'
                    for index, cmd in enumerate(self.cmds):
                        if isinstance(cmd, tuple) and cmd[1] == to_replace:
                            cmds[index] = (cmd[0], replaced_by)
                    cmds = list(filter(lambda x: x != 'REMOVE', cmds))
                    self.cmds = cmds
            index += 1

    # aux methods
    def get_label_successor(self, label_index):
        if label_index == len(self.cmds) - 1:
            return None
        else:
            return self.cmds[label_index + 1]

    def get_jump_predecessor(self, jump_index):
        if jump_index == 0:
            return 'start'
        elif isinstance(self.cmds[jump_index - 1], tuple):
            return 'jump'
        else:
            return self.cmds[jump_index - 1]
