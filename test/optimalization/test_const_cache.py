from test.compiler_test_case import CompilerTestCase


class TestConstCache(CompilerTestCase):
    def test_should_properly_cache_constants(self):
        self.assertOutputEquals(
            CONST_CACHE,
            '128\n128\n128\n128\n128\n128'
        )


CONST_CACHE = """
VAR
    a b
BEGIN
    a := 128;
    WRITE a;
    a := 128;
    WRITE a;
    a := 128;
    WRITE a;
    a := 128;
    WRITE a;
    a := 128;
    WRITE a;
    a := 128;
    WRITE a;
    a := 128;
END
"""
