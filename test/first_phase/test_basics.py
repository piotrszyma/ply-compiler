from test.compiler_test_case import CompilerTestCase


class TestOperations(CompilerTestCase):
    def test_assign_should_work(self):
        self.assertOutputEquals(
            CLASSIC,
            '1'
        )


CLASSIC = """
VAR
    a b
BEGIN
    a := 1;
    b := a;
    WRITE b;
END
"""
