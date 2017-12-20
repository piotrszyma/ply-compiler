from test.compiler_test_case import CompilerTestCase


class TestOperations(CompilerTestCase):
    def test_addition_should_work(self):
        self.assertEqual(
            self.compile_and_run(MIX_ADDITION),
            '10'
        )

        self.assertEqual(
            self.compile_and_run(NUMBER_VAR_ADDITION),
            '6'
        )

        self.assertEqual(
            self.compile_and_run(VAR_NUMBER_ADDITION),
            '6'
        )

        self.assertEqual(
            self.compile_and_run(TWO_VARS_ADDITION),
            '11'
        )

        self.assertEqual(
            self.compile_and_run(TWO_TAB_ELS_ADDITION),
            '4'
        )

    def test_substraction_should_work(self):
        self.assertEqual(
            self.compile_and_run(NUM_SUBST),
            '3'
        )
        self.assertEqual(
            self.compile_and_run(VAR_SUBST),
            '11'
        )

        self.assertEqual(
            self.compile_and_run(MIX_SUBSTRACTION),
            '1'
        )


NUM_SUBST = """
VAR
    a
BEGIN
    a := 5 - 2; (a=3)
    WRITE a;
END
"""

VAR_SUBST = """
VAR
    a b
BEGIN
    a := 3;
    b := 8;
    a := a + b;
    WRITE a; (a=11)
END"""

MIX_SUBSTRACTION = """
VAR
    a b[10]
BEGIN
    a := 3 - 2; (a=3)
    a := a - 100;
    b[0] := 200;
    b[1] := 199;
    b[2] := b[0] - b[1]; (b[2] = 1)
    b[2] := b[2] + a; (b[2] = 1)
    WRITE b[2];
END
"""

MIX_ADDITION = """
VAR
    a b c[10]
BEGIN
    a := 1 + 2; (a=3)
    b := 1 + a; (b=4)
    c[0] := 3; 
    b := b + c[0]; (b=7)
    c[9] := c[0] + b; (c[9]=10)
    WRITE c[9]; (10)
END
"""

VAR_NUMBER_ADDITION = """
VAR
    a
BEGIN
    a := 5;
    a := a + 1;
    WRITE a;
END
"""

NUMBER_VAR_ADDITION = """
VAR
    a
BEGIN
    a := 5;
    a := 1 + a;
    WRITE a;
END
"""

TWO_VARS_ADDITION = """
VAR
    a b
BEGIN
    a := 5;
    b := 6;
    a := a + b;
    WRITE a;
END
"""

TWO_TAB_ELS_ADDITION = """
VAR
    a[10]
BEGIN
    a[0] := 1;
    a[2] := 3;
    a[1] := a[0] + a[2];
    WRITE a[1];
END
"""
