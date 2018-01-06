import pytest

from test.compiler_test_case import CompilerTestCase


class TestOperations(CompilerTestCase):
    def test_addition_should_work(self):
        self.assertEqual(
            self.compileAndRun(MIX_ADDITION),
            '10'
        )

        self.assertEqual(
            self.compileAndRun(NUMBER_VAR_ADDITION),
            '6'
        )

        self.assertEqual(
            self.compileAndRun(VAR_NUMBER_ADDITION),
            '6'
        )

        self.assertEqual(
            self.compileAndRun(TWO_VARS_ADDITION),
            '11'
        )

        self.assertEqual(
            self.compileAndRun(TWO_TAB_ELS_ADDITION),
            '4'
        )

    def test_substraction_should_work(self):
        self.assertEqual(
            self.compileAndRun(NUM_SUBST),
            '3'
        )
        self.assertEqual(
            self.compileAndRun(VAR_SUBST),
            '11'
        )

        self.assertEqual(
            self.compileAndRun(MIX_SUBSTRACTION),
            '1'
        )

    def test_multiplication_should_work(self):
        self.assertEqual(
            self.compileAndRun(NUM_MULT),
            '246'
        )

        self.assertEqual(
            self.compileAndRun(TEST_MUL),
            '35\n10\n10\n49\n49\n49\n49\n49\n14\n28\n28\n8\n49\n14\n4'
        )

        self.assertEqual(
            self.compileAndRun(SHOULD_NOT_WRITE),
            ''
        )

    def test_division_should_work(self):
        self.assertOutputEquals(
            self.compileAndRun(DIV_ONE),
            "2\n1\n3\n2\n0\n2\n2\n1\n2\n1\n1\n2\n1\n3\n1\n0\n1\n3\n1\n0\n1\n1\n1\n1\n0\n3"
        )

    def test_operations_should_work(self):
        self.assertOutputEquals(
            MIX_SEC,
            '4\n4\n5\n9\n3\n3\n1\n1\n8\n8\n1\n1\n0\n0'
        )
        self.assertOutputEquals(
            OP_MIX,
            '13\n7\n30\n3\n1'
        )

        self.assertOutputEquals(
            TEST_OP_MAX,
            '19999999998\n0\n1\n7766279611452241921'
        )

    def test_modulo_should_work(self):
        self.assertOutputEquals(
            TEST_MOD,
            '0\n2\n0\n1\n2\n0\n6\n0\n1\n0\n0\n1\n0\n2\n0\n4\n0\n1\n0\n2\n3\n0\n3\n0\n2\n0'
        )

    def test_div(self):
        stmt = """
        a := {first} / {second};
        IF a <> {result} THEN WRITE 1; ENDIF
        """
        stmts = []

        for first in range(0, 10):
            for second in range(0, 10):
                result = (first // second) if second != 0 else 0

                stmts.append(stmt.format(first=first, second=second, result=result))

        body = "\n".join(stmts)

        code = """
        VAR
            a b c d
        BEGIN
            {body}
        END
        """.format(body=body)
        self.assertOutputEquals(
            code,
            ''
        )

    def test_mod(self):
        stmt = """
        a := {first} % {second};
        IF a <> {result} THEN WRITE 1; ENDIF
        """
        stmts = []

        for first in range(100, 110):
            for second in range(0, 10):
                result = (first % second) if second != 0 else 0
                stmts.append(stmt.format(first=first, second=second, result=result))

        body = "\n".join(stmts)

        code = """
        VAR
            a b c d
        BEGIN
            {body}
        END
        """.format(body=body)
        self.assertOutputEquals(
            code,
            ''
        )

    def test_add(self):
        stmt = """
        a := {first} + {second};
        IF a <> {result} THEN WRITE 1; ENDIF
        """
        stmts = []

        for first in range(100, 110):
            for second in range(0, 10):
                result = first + second
                stmts.append(stmt.format(first=first, second=second, result=result))

        body = "\n".join(stmts)

        code = """
        VAR
            a b c d
        BEGIN
            {body}
        END
        """.format(body=body)
        self.assertOutputEquals(
            code,
            ''
        )

    def test_sub(self):
        stmt = """
        a := {first} - {second};
        IF a <> {result} THEN WRITE 1; ENDIF
        """
        stmts = []

        for first in range(100, 110):
            for second in range(0, 10):
                result = first - second
                stmts.append(stmt.format(first=first, second=second, result=result))

        body = "\n".join(stmts)

        code = """
        VAR
            a b c d
        BEGIN
            {body}
        END
        """.format(body=body)
        self.assertOutputEquals(
            code,
            ''
        )


SHOULD_NOT_WRITE = """
VAR
    a b c
BEGIN
    a := 10 * 10;

    IF a <> 100 THEN
        WRITE 1;
    ENDIF

    a := 10 * 0;

    IF a <> 0 THEN
        WRITE 1;
    ENDIF

    a := 10 * 11;

    IF a <> 110 THEN
        WRITE 1;
    ENDIF

END
"""

TEST_OP_MAX = """
VAR
    a b c
BEGIN

   a := 9999999999;
   b := 9999999999;
   c := a+b;
   WRITE c;
   c := a-b;
   WRITE c;
   c := a/b;
   WRITE c;
   c := a*b;
   WRITE c;

END
"""

TEST_MUL = """
VAR
    a b array[5] result one zero
BEGIN

    a    := 2;
    b    := 2;
    one  := 1;
    zero := 0;
    array[0] := 4;
    array[1] := 7;


    result := 5 * 7;
    WRITE result; (35)

    result := 5 * a;
    WRITE result;(10)

    result := a * 5;
    WRITE result; (10)

    result := 7 * array[1];
    WRITE result; (49)

    result := array[1] * 7;
    WRITE result; (49)

    result := 7 * array[one];
    WRITE result; (49)

    result := array[one] * 7;
    WRITE result; (49)

    result := array[1] * array[1];
    WRITE result; (49)

    result := array[one] * b;
    WRITE result; (14)

    result := array[one] * array[zero];
    WRITE result; (28)

    result := array[one] * array[0];
    WRITE result; (28)

    result := a * array[zero];
    WRITE result; (8)

    result := array[1] * array[one];
    WRITE result; (49)

    result := a * array[1];
    WRITE result; (14)

    result := a * b;
    WRITE result; (4)

END
"""

TEST_MOD = """
VAR
    a b array[5] result one zero
BEGIN

    a    := 2;
    b    := 7;
    one  := 1;
    zero := 0;
    array[0] := 4;
    array[1] := 7;


    result := 6 % 3;
    WRITE result; (0)

    result := 6 % 4;
    WRITE result; (2)

    result := 6 % a;
    WRITE result;(0)

    result := 5 % a;
    WRITE result; (1)

    result := a % 5;
    WRITE result; (2)

    result := a % 1;
    WRITE result; (0)

    result := 20 % array[1];
    WRITE result; (6)

    result := 7 % array[1];
    WRITE result; (0)

    result := array[1] % 3;
    WRITE result; (1)

    result := array[1] % 7;
    WRITE result; (0)

    result := 7 % array[one];
    WRITE result; (0)

    result := 15 % array[one];
    WRITE result; (1)

    result := array[one] % 7;
    WRITE result; (0)

    result := array[one] % 5;
    WRITE result; (2)

    result := array[1] % array[1];
    WRITE result; (0)

    result := array[0] % array[1];
    WRITE result; (4)

    result := array[one] % b;
    WRITE result; (0)

    result := array[one] % a;
    WRITE result; (1)

    result := b % array[one];
    WRITE result; (0)

    result := a % array[one];
    WRITE result; (2)

    result := array[one] % array[zero];
    WRITE result; (3)

    result := array[one] % array[one];
    WRITE result; (0)

    result := array[one] % array[0];
    WRITE result; (3)

    result := array[1] % array[one];
    WRITE result; (0)

    result := a % b;
    WRITE result; (2)

    result := b % b;
    WRITE result; (0)
END
"""

MIX_SEC = """
VAR
a b c f g h i j s t u w d[33] e[22] k l m n o p r
BEGIN
  a := 1;
  b := 10;
  d[1] := 1;
  e[1] := 2;

  f := 5 - 1;
  g := 5 - a;
  h := b - 5;
  i := b - a;
  j := 5 - e[1];
  k := 5 - e[a];

  l := e[1] - 1;
  m := e[a] - 1;
  o := b - e[1];
  p := b - e[a];

  r := e[1] - a;
  s := e[a] - a;
  t := e[1] - e[a];
  u := e[a] - e[1];

  WRITE f; (4)
  WRITE g; (4)
  WRITE h; (5)
  WRITE i; (9)
  WRITE j; (3)
  WRITE k; (3)
  WRITE l; (1)
  WRITE m; (1)
  WRITE o; (8)
  WRITE p; (8)
  WRITE r; (1)
  WRITE s; (1)
  WRITE t; (0)
  WRITE u; (0)
END
"""

OP_MIX = """
VAR
    a b c
BEGIN
    a := 10;
    b := 3;
    c := a + b; WRITE c; (13)
    c := a - b; WRITE c; (7)
    c := a * b; WRITE c; (30)
    c := a / b; WRITE c; (3)
    c := a % b; WRITE c; (1)
END"""

NUM_MULT = """
VAR
    a b
BEGIN
    b := 2;
    a := 123;
    a := a * b;
    WRITE a;
END
"""

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

DIV_ONE = """
VAR
    a b array[5] result one zero
BEGIN

    a    := 2;
    b    := 7;
    one  := 1;
    zero := 0;
    array[0] := 4;
    array[1] := 7;


    result := 6 / 3;
    WRITE result; (2)

    result := 6 / 5;
    WRITE result; (1)

    result := 6 / a;
    WRITE result;(3)

    result := 5 / a;
    WRITE result; (2)

    result := a / 5;
    WRITE result; (0)

    result := a / 1;
    WRITE result; (2)

    result := 15 / array[1];
    WRITE result; (2)

    result := 7 / array[1];
    WRITE result; (1)

    result := array[1] / 3;
    WRITE result; (2)

    result := array[1] / 7;
    WRITE result; (1)

    result := 7 / array[one];
    WRITE result; (1)

    result := 15 / array[one];
    WRITE result; (2)

    result := array[one] / 7;
    WRITE result; (1)

    result := array[one] / 2;
    WRITE result; (3)

    result := array[1] / array[1];
    WRITE result; (1)

    result := array[0] / array[1];
    WRITE result; (0)

    result := array[one] / b;
    WRITE result; (1)

    result := array[one] / a;
    WRITE result; (3)

    result := b / array[one];
    WRITE result; (1)

    result := a / array[one];
    WRITE result; (0)

    result := array[one] / array[zero];
    WRITE result; (1)

    result := array[one] / array[0];
    WRITE result; (1)

    result := array[1] / array[one];
    WRITE result; (1)

    result := array[one] / array[zero];
    WRITE result; (1)

    result := a / b;
    WRITE result; (0)

    result := b / a;
    WRITE result; (3)

END
"""
