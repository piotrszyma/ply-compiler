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
