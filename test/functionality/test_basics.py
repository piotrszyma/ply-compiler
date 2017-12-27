from test.compiler_test_case import CompilerTestCase


class TestOperations(CompilerTestCase):
    def test_assign_should_work(self):
        self.assertOutputEquals(
            CLASSIC,
            '1'
        )

    def test_array_assignment(self):
        self.assertOutputEquals(
            ARR_ASSIGNMENT,
            '3'
        )

        self.assertOutputEquals(
            ARR_ASS_2,
            '123'
        )

        self.assertOutputEquals(
            ARR_ASS_3,
            '1\n2\n3'
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

ARR_ASSIGNMENT = """
VAR
    a[5] b
BEGIN
    b := 0;
    a[b] := 3;
    WRITE a[0];
END
"""

ARR_ASS_2 = """
VAR
    a[5] b c
BEGIN
    b := 0;
    a[b] := 123;
    b := 1;
    c := 0;
    a[b] := a[c];
    WRITE a[b];
END
"""


ARR_ASS_3 = """
VAR
    a[5] b c
BEGIN
    FOR i FROM 1 TO 3 DO
        a[i] := i;
        WRITE i;
    ENDFOR
END
"""
