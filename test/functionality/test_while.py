from test.compiler_test_case import CompilerTestCase


class TestWhileLoop(CompilerTestCase):
    def test_loop_should_work(self):
        self.assertEqual(
            self.compileAndRun(CLASSIC),
            '0\n1\n2'
        )


CLASSIC = """
VAR
    a b
BEGIN
    a := 3;
    b := 0;
    WHILE a <> b DO
        WRITE b;
        b := b + 1;
    ENDWHILE
END
"""
