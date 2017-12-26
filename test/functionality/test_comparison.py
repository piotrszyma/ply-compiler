from test.compiler_test_case import CompilerTestCase


class TestComparisons(CompilerTestCase):
    def test_lt_operator(self):
        self.assertOutputEquals(
            LESS,
            '0'
        )

    def test_leq_operator(self):
        self.assertOutputEquals(
            LESS_OR_EQUAL,
            '1'
        )

    def test_gt_operator(self):
        self.assertOutputEquals(
            GREATER,
            '1'
        )

    def test_geq_operator(self):
        self.assertOutputEquals(
            GEQ,
            '6'
        )

        self.assertOutputEquals(
            GREATER_OR_EQUAL,
            '6\n6\n6'
        )

    def test_eq_operator(self):
        self.assertOutputEquals(
            EQUALS,
            '1'
        )

    def test_compare_mix(self):
        self.assertOutputEquals(
            MIX,
            '2\n3'
        )


MIX = """
VAR
    a b
BEGIN
    a := 23;
    b := 121;
    IF a = b THEN
        WRITE 1;
    ENDIF
    IF a <> b THEN
        WRITE 2;
    ENDIF
    IF a <= b THEN
        WRITE 3;
    ENDIF
    IF a > b THEN
        WRITE 4;
    ENDIF
END
"""

EQUALS = """
VAR
    a b
BEGIN
    a := 2;
    b := 2;
    IF a = b THEN
        WRITE 1;
    ENDIF
END
"""

LESS = """
VAR
    a b
BEGIN
    a := 3;
    b := 2;
    IF a < b THEN
        WRITE 1;
    ELSE
        WRITE 0;
    ENDIF
END
"""

LESS_OR_EQUAL = """
VAR
    a b
BEGIN
    a := 100;
    b := 100;
    IF a <= b THEN
        WRITE 1;
    ENDIF
END
"""

GEQ = """
VAR
    a b
BEGIN
    a := 3;
    b := 4;
    IF a >= b THEN
        WRITE 12;
    ELSE
        WRITE 6;
    ENDIF
END"""

GREATER_OR_EQUAL = """
VAR
    a b
BEGIN
    a := 3;
    b := 4;
    IF a >= b THEN
        WRITE 12;
    ELSE
        WRITE 6;
    ENDIF
    
    IF a = b THEN
        WRITE 12;
    ELSE
        WRITE 6;
    ENDIF
    
    IF a > b THEN
        WRITE 12;
    ELSE
        WRITE 6;
    ENDIF
END
"""

GREATER = """
VAR
    a b
BEGIN
    a := 3;
    b := 2;
    IF a > b THEN
        WRITE 1;
    ELSE
        WRITE 0;
    ENDIF
END
"""
