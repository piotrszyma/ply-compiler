import ply.lex as lex


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
        'ASSIGNMENT',
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

        'LEFTBRACKET',
        'RIGHTBRACKET',
        'COMMENT'
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
    t_ASSIGNMENT = r':='
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

    t_LEFTBRACKET = r'\['
    t_RIGHTBRACKET = r'\]'

    t_ignore_COMMENT = r'\(.*\)'
    t_ignore = ' \r\t'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])

    def tokenize(self, source_code):
        self.lexer.input(source_code)
        while True:
            t = self.lexer.token()
            if t:
                yield t
            else:
                break

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
