from test.compiler_test_case import CompilerTestCase


class TestComparisons(CompilerTestCase):
    def test_lt_operator(self):
        self.assertOutputEquals(
            LESS,
            '0'
        )

        self.assertOutputEquals(
            ALTB,
            '1\n2\n3\n4\n5\n6\n7\n8\n9'
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
        self.assertOutputEquals(
            AGTB,
            '1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12'
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

        self.assertOutputEquals(
            AGEQB,
            '1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22'
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


ALTB = """
VAR
    a b c[10] d e
BEGIN
    a := 1;
    b := 2;
    IF 0 < a THEN WRITE 1; ENDIF
    IF 1 < a THEN WRITE 101; ENDIF
    IF 2 < a THEN WRITE 102; ENDIF
    IF a < 0 THEN WRITE 103; ENDIF
    IF a < 1 THEN WRITE 104; ENDIF
    IF a < 2 THEN WRITE 2; ENDIF

    b := 2;
    IF a < b THEN WRITE 3; ENDIF
    b := 1;
    IF a < b THEN WRITE 105; ENDIF
    b := 0;
    IF a < b THEN WRITE 106; ENDIF


    b := 2;
    IF d < a THEN WRITE 4; ENDIF


    c[0] := 0;
    IF a < c[0] THEN WRITE 107; ENDIF
    c[0] := 1;
    IF a < c[0] THEN WRITE 108; ENDIF
    c[0] := 2;
    IF a < c[0] THEN WRITE 5; ENDIF


    c[1] := 0;
    IF c[1] < a THEN WRITE 6; ENDIF
    c[1] := 1;
    IF c[1] < a THEN WRITE 109; ENDIF
    c[1] := 2;
    IF c[1] < a THEN WRITE 110; ENDIF


    d := 0;
    e := 1;
    c[d] := 2;
    IF a < c[d] THEN WRITE 7; ENDIF
    c[e] := 0;
    IF c[e] < a THEN WRITE 8; ENDIF
    c[e] := 1;
    IF c[e] < a THEN WRITE 111; ENDIF
    c[e] := 2;
    IF c[e] < a THEN WRITE 112; ENDIF


    IF 0 < 1 THEN WRITE 9; ENDIF
    IF 1 < 1 THEN WRITE 113; ENDIF
    IF 2 < 1 THEN WRITE 114; ENDIF
END
"""

AGTB = """
VAR
    a b c[10] d e
BEGIN
    a := 2;
    IF 0 > a THEN WRITE 100; ENDIF
    IF 1 > a THEN WRITE 101; ENDIF
    IF 2 > a THEN WRITE 102; ENDIF
    IF 3 > a THEN WRITE 1; ENDIF
    IF a > 0 THEN WRITE 2; ENDIF
    IF a > 1 THEN WRITE 3; ENDIF
    IF a > 2 THEN WRITE 103; ENDIF
    IF a > 3 THEN WRITE 104; ENDIF

    b := 0;
    IF a > b THEN WRITE 4; ENDIF
    b := 1;
    IF a > b THEN WRITE 5; ENDIF
    b := 2;
    IF a > b THEN WRITE 105; ENDIF
    b := 3;
    IF a > b THEN WRITE 106; ENDIF


    c[0] := 0;
    IF a > c[0] THEN WRITE 6; ENDIF
    c[0] := 1;
    IF a > c[0] THEN WRITE 7; ENDIF
    c[0] := 2;
    IF a > c[0] THEN WRITE 107; ENDIF
    c[0] := 3;
    IF a > c[0] THEN WRITE 108; ENDIF

    c[1] := 0;
    IF c[1] > a THEN WRITE 109; ENDIF
    c[1] := 1;
    IF c[1] > a THEN WRITE 110; ENDIF
    c[1] := 2;
    IF c[1] > a THEN WRITE 111; ENDIF
    c[1] := 3;
    IF c[1] > a THEN WRITE 8; ENDIF


    d := 0;
    e := 1;

    c[d] := 0;
    IF a > c[d] THEN WRITE 9; ENDIF
    c[d] := 1;
    IF a > c[d] THEN WRITE 10; ENDIF
    c[d] := 2;
    IF a > c[d] THEN WRITE 112; ENDIF
    c[d] := 3;
    IF a > c[d] THEN WRITE 113; ENDIF

    c[e] := 0;
    IF c[e] > a THEN WRITE 114; ENDIF
    c[e] := 1;
    IF c[e] > a THEN WRITE 115; ENDIF
    c[e] := 2;
    IF c[e] > a THEN WRITE 116; ENDIF
    c[e] := 3;
    IF c[e] > a THEN WRITE 11; ENDIF

    IF 0 > 2 THEN WRITE 117; ENDIF
    IF 1 > 2 THEN WRITE 118; ENDIF
    IF 2 > 2 THEN WRITE 119; ENDIF
    IF 3 > 2 THEN WRITE 12; ENDIF
END
"""

AGEQB = """
VAR
    a b c[10] d e
BEGIN
    a := 2;
    IF 0 >= a THEN WRITE 100; ENDIF
    IF 1 >= a THEN WRITE 101; ENDIF
    IF 2 >= a THEN WRITE 1; ENDIF
    IF 3 >= a THEN WRITE 2; ENDIF

    IF 1 >= a THEN WRITE 103; ENDIF
    IF 2 >= a THEN WRITE 3; ENDIF
    IF 3 >= a THEN WRITE 4; ENDIF
    IF a >= 0 THEN WRITE 5; ENDIF
    IF a >= 1 THEN WRITE 6; ENDIF
    IF a >= 2 THEN WRITE 7; ENDIF
    IF a >= 3 THEN WRITE 104; ENDIF

    b := 0;
    IF a >= b THEN WRITE 8; ENDIF
    b := 1;
    IF a >= b THEN WRITE 9; ENDIF
    b := 2;
    IF a >= b THEN WRITE 10; ENDIF
    b := 3;
    IF a >= b THEN WRITE 105; ENDIF


    c[0] := 0;
    IF a >= c[0] THEN WRITE 11; ENDIF
    c[0] := 1;
    IF a >= c[0] THEN WRITE 12; ENDIF
    c[0] := 2;
    IF a >= c[0] THEN WRITE 13; ENDIF
    c[0] := 3;
    IF a >= c[0] THEN WRITE 106; ENDIF

    c[1] := 0;
    IF c[1] >= a THEN WRITE 107; ENDIF
    c[1] := 1;
    IF c[1] >= a THEN WRITE 108; ENDIF
    c[1] := 2;
    IF c[1] >= a THEN WRITE 14; ENDIF
    c[1] := 3;
    IF c[1] >= a THEN WRITE 15; ENDIF


    d := 0;
    e := 1;

    c[d] := 0;
    IF a >= c[d] THEN WRITE 16; ENDIF
    c[d] := 1;
    IF a >= c[d] THEN WRITE 17; ENDIF
    c[d] := 2;
    IF a >= c[d] THEN WRITE 18; ENDIF
    c[d] := 3;
    IF a >= c[d] THEN WRITE 109; ENDIF

    c[e] := 0;
    IF c[e] >= a THEN WRITE 110; ENDIF
    c[e] := 1;
    IF c[e] >= a THEN WRITE 111; ENDIF
    c[e] := 2;
    IF c[e] >= a THEN WRITE 19; ENDIF
    c[e] := 3;
    IF c[e] >= a THEN WRITE 20; ENDIF

    IF 0 >= 2 THEN WRITE 112; ENDIF
    IF 1 >= 2 THEN WRITE 113; ENDIF
    IF 2 >= 2 THEN WRITE 21; ENDIF
    IF 3 >= 2 THEN WRITE 22; ENDIF
END

"""

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
