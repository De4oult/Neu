from core.errors    import Position, UndefinedToken, ExpectedChar
from core.constants import NUMBERS, LET_NUM, LETTERS
from core.tokens    import Token, KeywordTokens


class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.filename = filename
        self.text     = text                                # input script
        self.pos      = Position(-1, 0, -1, filename, text) # cursor position
        self.char     = None                                # current char
        
        self.next()

    def next(self):
        self.pos.next(self.char)
        self.char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def tokenize(self):
        tokens: list[str] = []

        while self.char != None:
            if self.is_number():
                tokens.append(self.make_number())

            elif self.is_letter():
                tokens.append(self.make_identifier())

            elif self.char in ' \t':
                self.next()


            # PARSE OPERATORS

            elif self.char == '+':
                tokens.append(Token('PLUS', start = self.pos))
                self.next()
            
            elif self.char == '-':
                tokens.append(Token('MINUS', start = self.pos))
                self.next()
            
            elif self.char == '*':
                tokens.append(Token('STAR', start = self.pos))
                self.next()
            
            elif self.char == '/':
                tokens.append(Token('SLASH', start = self.pos))
                self.next()
            
            elif self.char == '^':
                tokens.append(Token('POW', start = self.pos))
                self.next()

            elif self.char == '(':
                tokens.append(Token('LPAREN', start = self.pos))
                self.next()
            
            elif self.char == ')':
                tokens.append(Token('RPAREN', start = self.pos))
                self.next()
            
            elif self.char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)

            elif self.char == '=':
                tokens.append(self.make_equals())

            elif self.char == '<':
                tokens.append(self.make_less_than())

            elif self.char == '>':
                tokens.append(self.make_greater_than())
            
            else:
                position_start = self.pos.copy()
                char           = self.char

                self.next()

                return [], UndefinedToken(
                    position_start,
                    self.pos,
                    f'`{char}`'
                ) # throw error: undefined token

        tokens.append(Token('EOF', start = self.pos))
        return tokens, None
    
    # MAKE METHODS

    def make_number(self) -> str: # function that convert tokens character into integer or float 
        number: str = ''
        dots  : int = 0
        start       = self.pos.copy()

        while (
            (self.char != None) and
            (self.char in NUMBERS + '.')
        ): 
            if self.char == '.':
                if dots == 1: break # throw error: invalid number
                dots   += 1
                number += '.'

                self.next()
                continue

            number += self.char
            self.next()

        if dots == 0:
            return Token('INT', int(number), start, self.pos)
        
        return Token('FLOAT', float(number), start, self.pos)
    
    def make_identifier(self):
        identifier: str = ''
        start           = self.pos.copy()

        while (
            (self.char != None) and
            (self.char in LET_NUM + '_')
        ):
            identifier += self.char
            self.next()

        token_type = 'KEYWORD' if (identifier in KeywordTokens) else 'IDENTIFIER'

        return Token(token_type, identifier, start, self.pos)

    def make_not_equals(self):
        start = self.pos.copy()
        self.next()

        if self.char == '=':
            self.next()
            return Token('NE', start = start, end = self.pos), None
        
        self.next()
        return None, ExpectedChar(start, self.pos, '`=` (after `!`)')

    def make_equals(self):
        token_type = 'EQ'
        start = self.pos.copy()
        self.next()

        if self.char == '=':
            self.next()
            token_type = 'EE'

        return Token(token_type, start = start, end = self.pos)
    
    def make_less_than(self):
        token_type = 'LT'
        start = self.pos.copy()
        self.next()

        if self.char == '=':
            self.next()
            token_type = 'LTE'

        return Token(token_type, start = start, end = self.pos)

    def make_greater_than(self):
        token_type = 'GT'
        start = self.pos.copy()
        self.next()

        if self.char == '=':
            self.next()
            token_type = 'GTE'

        return Token(token_type, start = start, end = self.pos)
    

    # BOOLEANS

    def is_number(self) -> bool: # check if token is integer or float
        return self.char in NUMBERS
    
    def is_letter(self) -> bool: # check if token is keyword or var_name
        return self.char in LETTERS
