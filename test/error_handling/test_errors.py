from test.compiler_test_case import CompilerTestCase


class TestErrors(CompilerTestCase):
    def test_should_throw_error(self):
        self.assertReturnCodeIsError(ERRORNEUS_CODE)
        self.assertReturnCodeIsError(UNDECLARED_VARIABLE)


ERRORNEUS_CODE = """
( Błąd w linii 3: druga deklaracja a )
VAR
  a b a
BEGIN
  READ a;
  b := a;
END
"""

UNDECLARED_VARIABLE = """
( Błąd w linii 5: niezadeklarowana zmienna a )
VAR
  b
BEGIN
  READ a;
  b := a;
END
"""