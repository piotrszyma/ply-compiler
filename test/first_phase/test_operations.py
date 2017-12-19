from test.compiler_test_case import CompilerTestCase


class TestAdditionOperation(CompilerTestCase):
    def test_should_add_numbers(self):
        result = self.compile_and_run(TWO_NUMBERS_ADDITION)
        self.assertEqual(result, '3')

    def test_should_add_number_to_variable(self):
        result = self.compile_and_run(NUMBER_VAR_ADDITION)
        self.assertEqual(result, '6')

    def test_should_add_two_variables(self):
        result = self.compile_and_run(TWO_VARS_ADDITION)
        self.assertEqual(result, '11')


TWO_NUMBERS_ADDITION = """
VAR
    a
BEGIN
    a := 1 + 2;
    WRITE a;
END
"""

NUMBER_VAR_ADDITION = """
VAR
    a
BEGIN
    a := 5;
    a := 1 + a;
    WRITE 6;
END
"""

TWO_VARS_ADDITION = """
VAR
    a b
BEGIN
    a := 5;
    b := 6;
    a := a + b;
    WRITE 11;
END
"""