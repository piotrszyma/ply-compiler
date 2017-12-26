from test.compiler_test_case import CompilerTestCase


class TestIfStatement(CompilerTestCase):
    def test_ifs_should_work(self):
        self.assertEqual(
            self.compileAndRun(IF_WITH_WRITE_IN_IF_WITH_WRITE),
            '1\n1'
        )

        self.assertEqual(
            self.compileAndRun(IF_WITH_WRITE_IN_IF),
            '1'
        )

        self.assertEqual(
            self.compileAndRun(IF_WITH_IF_WITH_ASSIGN),
            '7'
        )

    def test_nested_if_with_assign(self):
        self.assertEqual(
            self.compileAndRun(IF_WITH_IF_WITH_IF_WITH_ASSIGN),
            '7\n7\n7'
        )

        self.assertEqual(
            self.compileAndRun(IF_AFTER_IF_AFTER_IF),
            '31\n31\n31'
        )

    def test_if_else_should_work(self):
        self.assertEqual(
            self.compileAndRun(IF_ELSE_WITH_WRITES),
            '31'
        )

        self.assertEqual(
            self.compileAndRun(IF_ELSE_WITH_IF_ELSE_WRITES),
            '31'
        )

        self.assertEqual(
            self.compileAndRun(IF_ELSE_WITH_WRITES),
            '31'
        )


IF_AFTER_IF_AFTER_IF = """
VAR
    a b
BEGIN
    a := 31;
    b := 1;
    IF a <> b THEN
        WRITE a;
    ENDIF
    a := 31;
    b := 1;
    IF a <> b THEN
        WRITE a;
    ENDIF
    a := 31;
    b := 1;
    IF a <> b THEN
        WRITE a;
    ENDIF
END
"""

IF_ELSE_WITH_WRITES = """
VAR
    a b
BEGIN
    a := 31;
    b := 1;
    IF a <> b THEN
        WRITE a;
    ELSE
        WRITE b;
    ENDIF
END
"""

IF_ELSE_WITH_IF_ELSE_WRITES = """
VAR
    a b
BEGIN
    a := 31;
    b := 1;
    IF a <> b THEN
        b := 3;
        IF a <> b THEN
            b := 4;
            IF a <> b THEN
                b := 4;
                WRITE a;
            ELSE
                b := 3;
                WRITE b;
            ENDIF
        ELSE
            b := 3;
            WRITE b;
        ENDIF
    ELSE
        WRITE b;
    ENDIF
END
"""

IF_WITH_WRITE_IN_IF_WITH_WRITE = """
VAR
    a b
BEGIN
    a := 2;
    b := 1;
    IF a <> b THEN
        WRITE b;
        IF a <> b THEN
            WRITE b;
        ENDIF
    ENDIF
END
"""

IF_WITH_WRITE_IN_IF = """
VAR
    a b
BEGIN
    a := 2;
    b := 1;
    IF a <> b THEN
        IF a <> b THEN
            WRITE b;
        ENDIF
    ENDIF
END
"""

IF_WITH_IF_WITH_ASSIGN = """
VAR
    a b
BEGIN
    a := 2;
    b := 1;
    IF a <> b THEN
        IF a <> b THEN
            b := 7;
        ENDIF
    ENDIF
    WRITE b;
END
"""

IF_WITH_IF_WITH_IF_WITH_ASSIGN = """
VAR
    a b
BEGIN
    a := 2;
    b := 1;
    IF a <> b THEN
        IF a <> b THEN
            IF a <> b THEN
                IF a <> b THEN
                    b := 7;
                ENDIF
            ENDIF
        ENDIF
    ENDIF
    WRITE b;
        a := 2;
    b := 1;
    IF a <> b THEN
        IF a <> b THEN
            IF a <> b THEN
                IF a <> b THEN
                    b := 7;
                ENDIF
            ENDIF
        ENDIF
    ENDIF
    WRITE b;
    a := 2;
    b := 1;
    IF a <> b THEN
        IF a <> b THEN
            IF a <> b THEN
                IF a <> b THEN
                    b := 7;
                ENDIF
            ENDIF
        ENDIF
    ENDIF
    WRITE b;
END
"""
