from modules.constants import NUMBERS
from modules.tokens    import Token


class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text # input script
        self.pos  = -1   # text position
        self.char = None # current char
        self.next()

    def next(self):
        self.pos += 1
        self.char = self.text[self.pos] if self.pos < len(self.text) else None

    def tokenize(self):
        tokens: list[str] = []

        while self.char != None:
            match self.char:
                case ' \t':
                    self.next()

                #######################
                #   PARSE OPERATORS   #
                #######################
                case '+':
                    tokens.append(Token('PLUS'))
                    self.next()
                
                case '-':
                    tokens.append(Token('MINUS'))
                    self.next()
                
                case '*':
                    tokens.append(Token('STAR'))
                    self.next()
                
                case '/':
                    tokens.append(Token('SLASH'))
                    self.next()
                
                case '(':
                    tokens.append(Token('LPAREN'))
                    self.next()
                
                case ')':
                    tokens.append(Token('RPAREN'))
                    self.next()

                case _:
                    pass # throw error: undefined token
    
        return tokens
    
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
                continue

            number += self.char

        if dots == 0:
            return Token('INT', int(number))
        
        return Token('FLOAT', float(number))
    

    ################
    #   BOOLEANS   #
    ################
    def is_number(self) -> bool: # check if token is integer or float
        return self.make_number() in NUMBERS
