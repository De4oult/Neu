TokenTypes = {
    'INT'    : 'Int',
    'FLOAT'  : 'Float',
    'PLUS'   : 'Addition',
    'MINUS'  : 'Subtract',
    'STAR'   : 'Multiply',
    'SLASH'  : 'Divide',
    'LPAREN' : 'LParen',
    'RPAREN' : 'RParen'
}

class Token:
    def __init__(self, type: str, value: any = None) -> None:
        self.type  = TokenTypes.get(type)
        self.value = value

    def __repr__(self) -> str:
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'