TokenTypes = {
    'INT'        : 'Int',
    'FLOAT'      : 'Float',
    'PLUS'       : 'Addition',
    'MINUS'      : 'Subtract',
    'STAR'       : 'Multiply',
    'SLASH'      : 'Divide',
    'POW'        : 'Pow',
    'LPAREN'     : 'LParen',
    'RPAREN'     : 'RParen',
    'EQ'         : 'Assign',
    'KEYWORD'    : 'Keyword',
    'IDENTIFIER' : 'Identifier',
    'EOF'        : 'EndOfFile'
}

KeywordTokens = [
    'save'
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