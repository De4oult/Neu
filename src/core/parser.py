from core.tokens import TokenTypes
from core.nodes  import *

class Parser:
    def __init__(self, tokens: list) -> None:
        self.tokens      = tokens
        self.token_index = -1
        
        self.next()

    def next(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.token = self.tokens[self.token_index]
        
        return self.token
    
    def parse(self):
        return self.expression()
        
    ### TOKENS VALIDATORS

    def factor(self):
        token = self.token

        if token.type in (
            TokenTypes.get('INT'),
            TokenTypes.get('FLOAT')
        ):
            self.next()
            return NumberNode(token)

    def term(self):
        return self.binary_operation(self.factor, (
                TokenTypes.get('STAR'),
                TokenTypes.get('SLASH')
            )
        )

    def expression(self):
        return self.binary_operation(self.term, (
                TokenTypes.get('PLUS'),
                TokenTypes.get('MINUS')
            )
        )

    ### OPERATIONS

    def binary_operation(self, function, operators: tuple[str]):
        left = function()

        while self.token.type in operators:
            operator_token = self.token

            self.next()
            
            right = function()
            left  = BinaryOperationNode(left, operator_token, right) # change var name
    
        return left # change


class Result:
    def __init__(self) -> None:
        self.error = None
        self.node  = None

    def register(self, res):
        if isinstance(res, Result):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self
