from unittest import TestCase

import subprocess
import os

COMPILER_DIR = '/'.join(os.getcwd().split('/')[:-2])


class CompilerTestCase(TestCase):
    def compileAndRun(self, source):
        with open('test.tmp', 'w') as f:
            f.write(source)
        subprocess.run([COMPILER_DIR + '/plyc.py', './test.tmp'], stdout=subprocess.PIPE)
        r = subprocess.run([COMPILER_DIR + '/test/interpreter', './a.out'], stdout=subprocess.PIPE)
        self.assertEqual(r.returncode, 0)
        return "\n".join([s[2:] for s in str(r.stdout).split('\\n')[3:-2]])

    def compileAndRunWithStdin(self, source, stdin):
        with open('test.tmp', 'w') as f:
            f.write(source)
        subprocess.run([COMPILER_DIR + '/plyc.py', './test.tmp'], stdout=subprocess.PIPE)
        r = subprocess.run([COMPILER_DIR + '/test/interpreter', './a.out'], stdout=subprocess.PIPE,
                           input=stdin, encoding='utf-8')
        self.assertEqual(r.returncode, 0)
        return "\n".join([s[2:] for s in str(r.stdout).split('\n')[3:-2]])[2:]

    def assertReturnCodeIsError(self, source):
        with open('test.tmp', 'w') as f:
            f.write(source)
        r = subprocess.run([COMPILER_DIR + '/plyc.py', './test.tmp'], stdout=subprocess.PIPE)
        self.assertNotEqual(r.returncode, 0)

    def assertOutputEquals(self, source, expected_output, stdin=None):
        if stdin is None:
            self.assertEqual(
                self.compileAndRun(source),
                expected_output
            )
        else:
            self.assertEqual(
                self.compileAndRunWithStdin(source, stdin),
                expected_output
            )

    def getCodeFromFile(self, filename):
        filepath = COMPILER_DIR + '/test/jftt2017-testy/{}'.format(filename)
        with open(filepath, 'r') as f:
            out = f.read()
        return out
