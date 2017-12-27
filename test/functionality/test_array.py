from test.compiler_test_case import CompilerTestCase


class TestArray(CompilerTestCase):
    def test_should_properly_assign(self):
        self.assertOutputEquals(
            ARRAY_ASSIGNS,
            '3'
        )


ARRAY_ASSIGNS = """
VAR
    a[100] b
BEGIN
    b := 1;
    a[1] := 3;
    a[2] := a[b];
    WRITE a[2];
END
"""