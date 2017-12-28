from test.compiler_test_case import CompilerTestCase


class TestArray(CompilerTestCase):
    def test_should_properly_assign(self):
        self.assertOutputEquals(
            ARRAY_ASSIGNS,
            '3'
        )

    def test_should_properly_sum(self):
        self.assertOutputEquals(
            ARRAY_SUM,
            '7'
        )

    def test_should_properly_multiply(self):
        self.assertOutputEquals(
            ARRAY_MULT,
            '12'
        )


ARRAY_MULT = """
VAR
    a[5] b c
BEGIN
    a[0] := 3;
    a[1] := 4;
    b := 0;
    c := 1;
    a[b] := a[b] * a[c];
    WRITE a[b];
END
"""

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

ARRAY_SUM = """
VAR
    a[5] b c
BEGIN
    a[0] := 3;
    a[1] := 4;
    b := 0;
    c := 1;
    a[b] := a[b] + a[c];
    WRITE a[b];
END
"""