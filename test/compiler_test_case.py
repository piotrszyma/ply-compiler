from unittest import TestCase

import subprocess
import os

COMPILER_DIR = '/'.join(os.getcwd().split('/')[:-2])


class CompilerTestCase(TestCase):
    def compile_and_run(self, source):
        with open('test.tmp', 'w') as f:
            f.write(source)
        subprocess.run([COMPILER_DIR + '/plyc.py', './test.tmp'], stdout=subprocess.PIPE)
        r = subprocess.run([COMPILER_DIR + '/test/interpreter', './a.out'], stdout=subprocess.PIPE)
        # os.remove('a.out')
        # os.remove('test.tmp')
        return "\n".join([s[2:] for s in str(r.stdout).split('\\n')[3:-2]])
