from test.compiler_test_case import CompilerTestCase


class TestArray(CompilerTestCase):
    def test_should_properly_assign(self):
        pass


ARRAY_ASSIGNS = """
VAR
    a[100]
BEGIN
    a := 1;
    b := a;
    WRITE b;
END
"""