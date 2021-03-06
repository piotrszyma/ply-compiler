import ply.lex as lex

from lib.error import CompilerError


class Lexer:
    tokens = (
        'VAR',
        'BEGIN', 'END',
        'IF', 'THEN', 'ELSE', 'ENDIF',
        'WHILE', 'DO', 'ENDWHILE',
        'FOR', 'FROM', 'TO', 'ENDFOR',
        'DOWNTO',
        'READ',
        'WRITE',

        'PIDENTIFIER',
        'ASSIGN',
        'SEMICOLON',

        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'MODULO',
        'EQ',
        'NE',
        'LT',
        'GT',
        'LE',
        'GE',

        'LBRACKET',
        'RBRACKET'
    )

    t_VAR = r'VAR'
    t_BEGIN = r'BEGIN'
    t_END = r'END'
    t_IF = r'IF'
    t_THEN = r'THEN'
    t_ELSE = r'ELSE'
    t_ENDIF = r'ENDIF'
    t_WHILE = r'WHILE'
    t_DO = r'DO'
    t_ENDWHILE = r'ENDWHILE'
    t_FOR = r'FOR'
    t_FROM = r'FROM'
    t_TO = r'TO'
    t_ENDFOR = r'ENDFOR'
    t_DOWNTO = r'DOWNTO'
    t_READ = r'READ'
    t_WRITE = r'WRITE'

    t_PIDENTIFIER = r'[_a-z]+'
    t_ASSIGN = r':='
    t_SEMICOLON = r';'

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MODULO = r'%'
    t_EQ = r'='
    t_NE = r'<>'
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='

    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'

    t_ANY_ignore = ' \r\t'

    states = (
        ('comment', 'exclusive'),
    )

    def __init__(self):
        self.lexer = lex.lex(module=self)

    def tokenize(self, source_code):
        self.lexer.input(source_code)
        while True:
            t = self.lexer.token()
            if t:
                yield t
            else:
                break

    def t_START_COMMENT(self, t):
        r'\('
        self.lexer.begin('comment')

    def t_comment_END(self, t):
        r'\)'
        self.lexer.begin('INITIAL')

    def t_comment_CONTENT(self, t):
        r'.'
        pass

    def t_comment_eof(self, t):
        raise CompilerError(" In line %d: Unterminated comment" % t.lexer.lineno)

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_ANY_error(self, t):
        if t.value[0] == ')':
            error_msg = " In line {}: Are you trying to close unopened comment?".format(t.lexer.lineno)
        else:
            error_msg = " In line {}: Illegal character '{}'".format(t.lexer.lineno, t.value[0])
        raise CompilerError(error_msg)
