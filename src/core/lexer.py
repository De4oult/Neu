from core.errors    import Position, UndefinedToken
from core.constants import NUMBERS
from core.tokens    import Token


class Lexer:
    def __init__(self, filename: str, text: str) -> None:
        self.filename = filename
        self.text     = text                                 # input script
        self.pos      = Position(-1, 0, -1, filename, text) # cursor position
        self.char     = None                                 # current char
        
        self.next()

    def next(self):
        self.pos.next(self.char)
        self.char = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def tokenize(self):
        tokens: list[str] = []

        while self.char != None:
            if self.is_number():
                tokens.append(self.make_number())

            elif self.char in ' \t':
                self.next()


            #######################
            #   PARSE OPERATORS   #
            #######################

            elif self.char == '+':
                tokens.append(Token('PLUS'))
                self.next()
            
            elif self.char == '-':
                tokens.append(Token('MINUS'))
                self.next()
            
            elif self.char == '*':
                tokens.append(Token('STAR'))
                self.next()
            
            elif self.char == '/':
                tokens.append(Token('SLASH'))
                self.next()
            
            elif self.char == '(':
                tokens.append(Token('LPAREN'))
                self.next()
            
            elif self.char == ')':
                tokens.append(Token('RPAREN'))
                self.next()
            
            else:
                position_start = self.pos.copy()
                char           = self.char

                self.next()

                return [], UndefinedToken(
                    position_start,
                    self.pos,
                    f'`{char}`'
                ) # throw error: undefined token

        return tokens, None
    
    def make_number(self) -> str: # function that convert tokens character into integer or float 
        number: str = ''
        dots  : int = 0

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
            return Token('INT', int(number))
        
        return Token('FLOAT', float(number))
    

    ################
    #   BOOLEANS   #
    ################
    def is_number(self) -> bool: # check if token is integer or float
        return self.char in NUMBERS
