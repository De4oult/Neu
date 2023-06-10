from core.errors   import InvalidSyntax
from core.tokens   import TokenTypes
from core.observer import Result
from core.nodes    import *

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
        observer = self.expression()

        if not observer.error and self.token.type != TokenTypes.get('EOF'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    'operation expected (`+`, `-`, `*` or `/`)'
                )
            )

        return observer
        
    ### TOKENS VALIDATORS

    def factor(self):
        observer = Result()

        token = self.token

        if token.type in (
            TokenTypes.get('INT'),
            TokenTypes.get('FLOAT')
        ):
            observer.register(self.next())

            return observer.success(NumberNode(token))

        return observer.failure(
            InvalidSyntax(
                token.position_start,
                token.position_end,
                'integer or float expected'
            )
        )

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
        observer = Result()

        left = observer.register(function())
        if observer.error: return observer

        while self.token.type in operators:
            operator_token = self.token

            observer.register(self.next())
            
            right = observer.register(function())
            if observer.error: return observer
            
            left  = BinaryOperationNode(left, operator_token, right)
    
        return observer.success(left)
