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

        self.assertEqual(
            self.compileAndRun(WHILE_TESTS),
            ('4\n3\n2\n1\n0\n' * 18)[:-1]
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

WHILE_TESTS = """
VAR
    a b tablica[5] zero four six
BEGIN

    zero := 0;
    four := 4;
    six  := 6;

    tablica[0] := 0;
    tablica[1] := 1;
    tablica[2] := 2;
    tablica[3] := 3;
    tablica[4] := 4;

    FOR i FROM 4 DOWNTO 0 DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM 4 DOWNTO zero DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM four DOWNTO 0 DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[4] DOWNTO tablica[0] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[4] DOWNTO 0 DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM 4 DOWNTO tablica[0] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[four] DOWNTO zero DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[four] DOWNTO tablica[zero] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[four] DOWNTO 0 DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[four] DOWNTO tablica[0] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM 4 DOWNTO tablica[zero] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM four DOWNTO tablica[zero] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[4] DOWNTO tablica[zero] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[4] DOWNTO tablica[zero] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM four DOWNTO tablica[0] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM four DOWNTO tablica[0] DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM tablica[4] DOWNTO zero DO
        WRITE tablica[i];
    ENDFOR

    FOR i FROM four DOWNTO zero DO
        WRITE tablica[i];
    ENDFOR
END
"""
