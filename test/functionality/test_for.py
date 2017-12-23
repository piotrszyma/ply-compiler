from test.compiler_test_case import CompilerTestCase


class TestForLoop(CompilerTestCase):
    def test_for_up(self):
        self.assertOutputEquals(
            CLASSIC,
            '1\n2\n3'
        )


CLASSIC = """
VAR
    a b
BEGIN
    a := 1;
    b := 3;
    FOR i FROM a TO b DO
        WRITE i;
    ENDFOR
END
"""
