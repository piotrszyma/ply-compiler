import random

import pytest

from test.compiler_test_case import CompilerTestCase


class TestRandomOperations(CompilerTestCase):
    # @pytest.mark.skip
    def test_randomly_operations(self):
        operators = ['/', '+', '*', '%', '-']

        body = []

        variables = ['a[0]', 'a[b]']

        for first in range(0, 100):
            operation = random.choice(operators)
            left = random.randint(1000, 10000000)
            right = random.randint(1, 10000000)
            variable = random.choice(variables)

            stmt = """
            e[f] := {first};
            e[g] := {second};
            {variable} := e[f] {operation} e[g];
            IF {variable} = {result} THEN WRITE 1; ENDIF
            """

            expected_result = self.eval(operation, left, right)

            if expected_result < 0:
                expected_result = 0

            formated = stmt.format(first=left,
                                   second=right,
                                   operation=operation,
                                   result=expected_result,
                                   variable=variable
                                   )
            code = """
            VAR
                a[2] b c d e[10] f g sum
            BEGIN
                sum := 0;
                b := 0;
                f := 1;
                g := 2;
                {body}
            END
            """

            body.append(formated)
            try:

                self.assertOutputEquals(
                    code.format(body=formated),
                    '1'
                )
            except AssertionError as e:
                print(code.format(body=formated))
                raise AssertionError(e)

    # @pytest.mark.skip
    def test_for_loop(self):
        body = """
        VAR
            a[10] b c d e
        BEGIN
            {body}
        END
        """

        for _ in range(1, 100):
            stmt = """
            a[0] := {start};
            b := 1;
            a[b] := {end};
            FOR i FROM a[0] TO a[b] DO
                WRITE i;
            ENDFOR
            """

            first = random.randint(0, 100)
            second = random.randint(0, 100)

            expected = '\n'.join(map(lambda x: str(x), range(first, second + 1)))
            code = body.format(
                body=stmt.format(
                    start=first,
                    end=second
                )
            )

            with open("out", "w") as f:
                f.write(code)

            self.assertOutputEquals(
                body.format(
                    body=stmt.format(
                        start=first,
                        end=second
                    )
                ),
                expected
            )

    def eval(self, operation, left, right):
        op_map = {
            '+': lambda: left + right,
            '-': lambda: left - right if left - right > 0 else 0,
            '*': lambda: left * right,
            '/': lambda: 0 if right == 0 else left // right,
            '%': lambda: 0 if right == 0 else left % right
        }
        return op_map[operation]()
