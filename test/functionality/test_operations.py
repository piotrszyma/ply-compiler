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

    def test_operations_should_work(self):
        self.assertOutputEquals(
            MIX_SEC,
            '4\n4\n5\n9\n3\n3\n1\n1\n8\n8\n1\n1\n0\n0'
        )
        self.assertOutputEquals(
            OP_MIX,
            '13\n7\n30\n3\n1'
        )


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
