TokenTypes = {
    'INT'        : 'Int',
    'FLOAT'      : 'Float',
    'STRING'     : 'String',
    'PLUS'       : 'Addition',
    'MINUS'      : 'Subtract',
    'STAR'       : 'Multiply',
    'SLASH'      : 'Divide',
    'POW'        : 'Pow',
    'LPAREN'     : 'LParen',
    'RPAREN'     : 'RParen',
    'LBRACKET'   : 'LBracket',
    'RBRACKET'   : 'RBracket',
    'INC'        : 'Increment',
    'DEC'        : 'Decrement',
    'EQ'         : 'Assign',
    'EE'         : 'Equals',
    'NE'         : 'NotEquals',
    'LT'         : 'LessThan',
    'GT'         : 'GreaterThan',
    'LTE'        : 'LessThanOrEquals',
    'GTE'        : 'GreaterThanOrEquals',
    'KEYWORD'    : 'Keyword',
    'IDENTIFIER' : 'Identifier',
    'POINTER'    : 'Pointer',
    'LPOINTER'   : 'LPointer',
    'COMMA'      : 'Comma',
    'LSQUARE'    : 'LSquare',
    'RSQUARE'    : 'RSquare',
    'LBRACE'     : 'LBrace',
    'RBRACE'     : 'RBrace',
    'NEWLINE'    : 'NewLine',
    'EOF'        : 'EndOfFile'
}

KeywordTokens = [
    'save',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'for',
    'loop',
    'to',
    'break',
    'func'
]

class Token:
    def __init__(self, type: str, value: any = None, start = None, end = None) -> None:
        self.type  = TokenTypes.get(type)
        self.value = value

        if start:
            self.position_start = start.copy()
            self.position_end   = start.copy()
            self.position_end.next()

        if end: self.position_end = end

    def matches(self, type, value):
        return (self.type == type) and (self.value == value)

    def __repr__(self) -> str:
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'