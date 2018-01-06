import pytest

from test.compiler_test_case import CompilerTestCase


class TestForLoop(CompilerTestCase):
    def test_for_up(self):
        self.assertOutputEquals(
            CLASSIC_FORUP,
            '1\n2\n3'
        )
        self.assertOutputEquals(
            FORUP_OUT_OF_RANGE,
            ''
        )

    def test_for_down(self):
        self.assertOutputEquals(
            CLASSIC_FORDOWN,
            '3\n2\n1'
        )
        self.assertOutputEquals(
            CLASSIC_FORDOWN_OUT,
            ''
        )

    def test_loop_params_immutability(self):
        self.assertOutputEquals(
            IMMUTABILITY,
            '3\n5\n3\n4\n5\n3\n5\n5\n3'
        )

    def test_for_mix(self):
        self.assertOutputEquals(
            FOR_MIX_TESTS,
            ('4\n3\n2\n1\n0\n' * 18)[:-1]
        )


IMMUTABILITY = """
VAR
    a b
BEGIN
    a := 5;
    b := 3;
    FOR i FROM b TO a DO
        WRITE i;
        WRITE a;
        WRITE b;
    ENDFOR
END
"""

CLASSIC_FORUP = """
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

FORUP_OUT_OF_RANGE = """
VAR
    a b
BEGIN
    a := 3;
    b := 1;
    FOR i FROM a TO b DO
        WRITE i;
    ENDFOR
END
"""

CLASSIC_FORDOWN = """
VAR
    a b
BEGIN
    a := 3;
    b := 1;
    FOR i FROM a DOWNTO b DO
        WRITE i;
    ENDFOR
END
"""

CLASSIC_FORDOWN_OUT = """
VAR
    a b
BEGIN
    a := 3;
    b := 4;
    FOR i FROM a DOWNTO b DO
        WRITE i;
    ENDFOR
END
"""

FOR_MIX_TESTS = """
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
