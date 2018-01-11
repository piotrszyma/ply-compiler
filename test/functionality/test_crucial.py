import os

from test.compiler_test_case import CompilerTestCase

COMPILER_DIR = '/'.join(os.getcwd().split('/')[:-2])


class TestCrucial(CompilerTestCase):
    def test_program0(self):
        self.assertOutputEquals(
            self.getCodeFromFile('program0.imp'),
            '1\n0\n0\n0\n0\n0\n1\n0\n0\n0\n0\n1\n0\n0\n0\n1\n0\n0\n1\n0\n1',
            stdin='1345601\n'
        )

    def test_program1(self):
        self.assertOutputEquals(
            self.getCodeFromFile('program1.imp'),
            '2\n3\n5\n7\n11\n13\n17\n19\n23\n29\n31\n37\n41\n43\n47\n53\n59\n61\n67\n71\n73\n79\n83\n89\n97',
        )

    def test_program2(self):
        self.assertOutputEquals(
            self.getCodeFromFile('program2.imp'),
            '857\n1\n14405693\n1',
            stdin='12345678901\n'
        )

    def test_1_numbers(self):
        code = self.getCodeFromFile('1-numbers.imp')
        output = self.compileAndRunWithStdin(code, '20\n')
        self.assertEqual(
            ''.join(output.split('> ')),
            '1\n2\n10\n100\n10000\n1234567890\n35\n15\n999\n555555555\n7777\n999\n11\n707\n7777'
        )

    def test_2_fib(self):
        self.assertOutputEquals(
            self.getCodeFromFile('2-fib.imp'),
            '121393',
            stdin='1\n'
        )

    def test_3_fib_factorial(self):
        self.assertOutputEquals(
            self.getCodeFromFile('3-fib-factorial.imp'),
            '2432902008176640000\n17711',
            stdin='20\n'
        )

    def test_4_factorial(self):
        self.assertOutputEquals(
            self.getCodeFromFile('4-factorial.imp'),
            '2432902008176640000',
            stdin='20\n'
        )

    def test_5_tab(self):
        self.assertOutputEquals(
            self.getCodeFromFile('5-tab.imp'),
            '0\n23\n44\n63\n80\n95\n108\n119\n128\n135\n140\n143\n144\n143\n140\n135\n128\n119\n108\n95\n80\n63\n44'
            '\n23\n0',
        )

    def test_6_mod_mult(self):
        pass
