from test.compiler_test_case import CompilerTestCase


class TestWhileLoop(CompilerTestCase):
    def test_loop_should_work(self):
        self.assertEqual(
            self.compileAndRun(CLASSIC),
            '0\n1\n2\n0\n1\n2\n0\n1\n2\n0\n1\n2\n0\n1\n2'
        )

        self.assertEqual(
            self.compileAndRun(WITH_EQ),
            '4'
        )

        self.assertEqual(
            self.compileAndRun(MIX),
            '5'
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
    a := 3;
    b := 0;
    WHILE a <> b DO
        WRITE b;
        b := b + 1;
    ENDWHILE
    a := 3;
    b := 0;
    WHILE a <> b DO
        WRITE b;
        b := b + 1;
    ENDWHILE
    a := 3;
    b := 0;
    WHILE a <> b DO
        WRITE b;
        b := b + 1;
    ENDWHILE
    a := 3;
    b := 0;
        WHILE a <> b DO
        WRITE b;
        b := b + 1;
    ENDWHILE
END
"""

WITH_EQ = """
VAR
    a b
BEGIN
    a := 3;
    b := 3;
    WHILE a = b DO
        b := b + 1;
        WRITE b;
    ENDWHILE
END
"""

MIX = """
VAR
    a b
BEGIN
    a := 1;
    b := 5;
    WHILE a < b DO
        a := a + 1;
        IF a = b THEN
            WRITE a;
        ENDIF
    ENDWHILE
END
"""
