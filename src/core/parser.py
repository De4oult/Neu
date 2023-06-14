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
    
    def reverse(self, amount = 1):
        self.token_index -= amount
        self.update_token()

        return self.token
    
    def update_token(self):
        if self.token_index >= 0 and self.token_index < len(self.tokens):
            self.token = self.tokens[self.token_index]
    
    def parse(self):
        observer = self.statements()

        if not observer.error and self.token.type != TokenTypes.get('EOF'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    'operation expected (`+`, `-`, `*` or `/`)'
                )
            )

        return observer
        
    ### AST

    def if_expression(self):
        observer  = Result()
        cases     = []
        else_case = None

        if not self.token.matches(TokenTypes.get('KEYWORD'), 'if'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`if` expected'
                )
            )
        
        observer.register_next()
        self.next()

        condition = observer.register(self.expression())
        if observer.error: return observer

        if not self.token.type == TokenTypes.get('POINTER'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    'pointer `->` excpected'
                )
            )
        
        observer.register_next()
        self.next()

        expression = observer.register(self.expression())
        if observer.error: return observer
        
        cases.append((condition, expression))

        while self.token.matches(TokenTypes.get('KEYWORD'), 'elif'):
            observer.register_next()
            self.next()

            condition = observer.register(self.expression())
            if observer.error: return observer

            if not self.token.type == TokenTypes.get('POINTER'):
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        'pointer `->` excpected'
                    )
                )
            
            observer.register_next()
            self.next()

            expression = observer.register(self.expression())
            if observer.error: return observer

            cases.append((condition, expression))

        if self.token.matches(TokenTypes.get('KEYWORD'), 'else'):
            observer.register_next()
            self.next()

            else_case = observer.register(self.expression())
            if observer.error: return observer

        return observer.success(IfNode(cases, else_case))

    def for_expression(self):
        observer = Result()

        if not self.token.matches(TokenTypes.get('KEYWORD'), 'for'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`for` expected'
                )
            )
        
        observer.register_next()
        self.next()

        if self.token.type != TokenTypes.get('IDENTIFIER'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    'identifier expected'                    
                )
            )

        variable_name = self.token

        observer.register_next()
        self.next()

        if self.token.type != TokenTypes.get('EQ'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`=` expected'
                )
            )
        
        observer.register_next()
        self.next()

        start_value = observer.register(self.expression())
        if observer.error: return observer

        if not self.token.matches(TokenTypes.get('KEYWORD'), 'to'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`to` expected'
                )
            )
        
        observer.register_next()
        self.next()

        end_value = observer.register(self.expression())
        if observer.error: return observer

        step_value = None

        if not self.token.type == TokenTypes.get('POINTER'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`->` expected'
                )
            )
        
        observer.register_next()
        self.next()

        body = observer.register(self.expression())
        if observer.error: return observer

        return observer.success(ForNode(variable_name, start_value, end_value, step_value, body))
            
    def loop_expression(self):
        observer = Result()

        if not self.token.matches(TokenTypes.get('KEYWORD'), 'loop'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`loop` expected'
                )
            )
        
        observer.register_next()
        self.next()

        condition = observer.register(self.expression())
        if observer.error: return observer

        if not self.token.type == TokenTypes.get('POINTER'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`->` expected'
                )
            )      
        
        observer.register_next()
        self.next()

        body = observer.register(self.expression())
        if observer.error: return observer

        return observer.success(LoopNode(condition, body))     

    def function_definition(self):
        observer = Result()

        if not self.token.matches(TokenTypes.get('KEYWORD'), 'func'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`func` expected'
                )
            )
        
        observer.register_next()
        self.next()

        if self.token.type == TokenTypes.get('IDENTIFIER'):
            function_name = self.token

            observer.register_next()
            self.next()

            if self.token.type != TokenTypes.get('LPAREN'):
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        '`(` expected'
                    )
                )
        
        else:
            function_name = None
            
            if self.token.type != TokenTypes.get('LPAREN'):
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        'identifier or `(` expected'
                    )
                )
            
        observer.register_next()
        self.next()

        arguments_names = []

        if self.token.type == TokenTypes.get('IDENTIFIER'):
            arguments_names.append(self.token)

            observer.register_next()
            self.next()

            while self.token.type == TokenTypes.get('COMMA'):
                observer.register_next()
                self.next()

                if self.token.type != TokenTypes.get('IDENTIFIER'):
                    return observer.failure(
                        InvalidSyntax(
                            self.token.position_start,
                            self.token.position_end,
                            'argument expected'
                        )
                    )
                
                arguments_names.append(self.token)

                observer.register_next()
                self.next()
            
            if self.token.type != TokenTypes.get('RPAREN'):
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        '`,` or `)` expected'
                    )
                )
        
        else:
            if self.token.type != TokenTypes.get('RPAREN'):
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        'argument or `)` expected'
                    )
                )
            
        observer.register_next()
        self.next()

        if self.token.type != TokenTypes.get('POINTER'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    'pointer expected'
                )
            )
        
        observer.register_next()
        self.next()

        node = observer.register(self.expression())
        if observer.error: return observer

        return observer.success(FunctionDefinitionNode(
                function_name,
                arguments_names,
                node
            )
        )
    
    def list_expression(self):
        observer = Result()

        elements = []
        start    = self.token.position_start.copy()

        if self.token.type != TokenTypes.get('LSQUARE'):
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    '`[` expected'
                )
            )
    
        observer.register_next()
        self.next()

        if self.token.type == TokenTypes.get('RSQUARE'):
            observer.register_next()
            self.next()

        else:
            elements.append(observer.register(self.expression()))
            if observer.error:
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        'expression expected'
                    )
                )
            
            while self.token.type == TokenTypes.get('COMMA'):
                observer.register_next()
                self.next()

                elements.append(observer.register(self.expression()))
                if observer.error: return observer

            if self.token.type != TokenTypes.get('RSQUARE'):
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        '`,` or `]` expected'
                    )
                )
            
            observer.register_next()
            self.next()

        return observer.success(
            ListNode(
                elements,
                start,
                self.token.position_end.copy()
            )
        )

    def atom(self):
        observer = Result()

        token = self.token

        if token.type in (
            TokenTypes.get('INT'),
            TokenTypes.get('FLOAT')
        ):
            observer.register_next()
            self.next()

            return observer.success(NumberNode(token))

        elif token.type == TokenTypes.get('STRING'):
            observer.register_next()
            self.next()

            return observer.success(StringNode(token))

        elif token.type == TokenTypes.get('IDENTIFIER'):
            observer.register_next()
            self.next()

            if self.token.type == TokenTypes.get('INC'):
                print('not allowed now')

            elif self.token.type == TokenTypes.get('DEC'):
                print('not allowed now')
            
            return observer.success(VariableAccessNode(token))

        elif token.type == TokenTypes.get('LPAREN'):
            observer.register_next()
            self.next()

            expression = observer.register(self.expression())

            if observer.error: return observer
            
            if self.token.type == TokenTypes.get('RPAREN'):
                observer.register_next()
                self.next()
                
                return observer.success(expression)
            
            else:
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start,
                        self.token.position_end,
                        '`)` expected'
                    )
                )

        elif token.type == TokenTypes.get('LSQUARE'):
            list_expression = observer.register(self.list_expression())
            if observer.error: return observer

            return observer.success(list_expression)
        
        elif token.matches(TokenTypes.get('KEYWORD'), 'if'):
            if_expression = observer.register(self.if_expression())
            if observer.error: return observer

            return observer.success(if_expression)

        elif token.matches(TokenTypes.get('KEYWORD'), 'for'):
            for_expression = observer.register(self.for_expression())
            if observer.error: return observer
            
            return observer.success(for_expression)

        elif token.matches(TokenTypes.get('KEYWORD'), 'loop'):
            loop_expression = observer.register(self.loop_expression())
            if observer.error: return observer
            
            return observer.success(loop_expression)
        
        elif token.matches(TokenTypes.get('KEYWORD'), 'func'):
            function_definition = observer.register(self.function_definition())
            if observer.error: return observer
            
            return observer.success(function_definition)
        
        return observer.failure(
            InvalidSyntax(
                token.position_start,
                token.position_end,
                'integer, float, identifier, `+`, `-` or `(` expected'
            )
        )

    def power(self):
        return self.binary_operation(self.call, (
                TokenTypes.get('POW'), 
            ),
            self.factor
        )

    def call(self):
        observer = Result()
        
        atom = observer.register(self.atom())
        if observer.error: return observer

        if self.token.type == TokenTypes.get('LPAREN'):
            observer.register_next()
            self.next()

            argument_nodes = []

            if self.token.type == TokenTypes.get('RPAREN'):
                observer.register_next()
                self.next()

            else:
                argument_nodes.append(observer.register(self.expression()))
                if observer.error:
                    return observer.failure(
                        InvalidSyntax(
                            self.token.position_start,
                            self.token.position_end,
                            'keyword or expression expected'            
                        )
                    )
                
                while self.token.type == TokenTypes.get('COMMA'):
                    observer.register_next()
                    self.next()

                    argument_nodes.append(observer.register(self.expression()))
                    if observer.error: return observer

                if self.token.type != TokenTypes.get('RPAREN'):
                    return observer.failure(
                        InvalidSyntax(
                            self.token.position_start,
                            self.token.position_end,
                            '`,` or `)` expected'
                        )
                    )
                
                observer.register_next()
                self.next()

            return observer.success(CallNode(atom, argument_nodes))

        return observer.success(atom)


    def factor(self):
        observer = Result()

        token = self.token

        if token.type in (
            TokenTypes.get('PLUS'),
            TokenTypes.get('MINUS'),
            TokenTypes.get('INC'),
            TokenTypes.get('DEC')
        ):
            observer.register_next()
            self.next()

            factor = observer.register(self.factor())
            if observer.error: return observer

            return observer.success(UnaryOperationNode(token, factor))

        return self.power()

    def term(self):
        return self.binary_operation(self.factor, (
                TokenTypes.get('STAR'),
                TokenTypes.get('SLASH')
            )
        )
    
    def arithmetical_expression(self):
        return self.binary_operation(self.term, (
                TokenTypes.get('PLUS'),
                TokenTypes.get('MINUS'),
                TokenTypes.get('INC'),
                TokenTypes.get('DEC')
            )
        )
    
    def compare_expression(self):
        observer = Result()

        if self.token.matches(TokenTypes.get('KEYWORD'), 'not'):
            operator = self.token
            
            observer.register_next()
            self.next()

            node = observer.register(self.compare_expression())
            if observer.error: return observer
            
            return observer.success(UnaryOperationNode(operator, node))
        
        node = observer.register(
            self.binary_operation(
                self.arithmetical_expression,
                (
                    TokenTypes.get('EE'),
                    TokenTypes.get('NE'),
                    TokenTypes.get('LT'),
                    TokenTypes.get('GT'),
                    TokenTypes.get('LTE'),
                    TokenTypes.get('GTE'),
                    TokenTypes.get('LPOINTER')
                )
            )
        )

        if observer.error:
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start,
                    self.token.position_end,
                    'integer, float, identifier, `+`, `-`, `not` or `(` expected'
                )
            )
        
        return observer.success(node)

    def statements(self):
        observer = Result()

        statements = []
        start      = self.token.position_start.copy()

        while self.token.type == TokenTypes.get('NEWLINE'):
            observer.register_next()
            self.next()

        statement = observer.register(self.expression())
        if observer.error: return observer

        statements.append(statement)

        more_statements = True

        while True:
            newlines = 0
            while self.token.type == TokenTypes.get('NEWLINE'):
                observer.register_next()
                self.next()

                newlines += 1
            
            if newlines == 0:
                more_statements = False

            if not more_statements: break

            statement = observer.try_register(self.expression())
            if not statement: 
                self.reverse(observer.reverse_count)
                more_statements = False

                continue

            statements.append(statement)

        return observer.success(
            ListNode(
                statements,
                start,
                self.token.position_end.copy()
            )
        )


    def expression(self):
        observer = Result()

        if self.token.matches(TokenTypes.get('KEYWORD'), 'save'):
            observer.register_next()
            self.next()

            if self.token.type != TokenTypes.get('IDENTIFIER'):
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start, 
                        self.token.position_end,
                        'identifier expected'
                    )
                )
            
            variable_name = self.token
            
            observer.register_next()
            self.next()

            if self.token.type != TokenTypes.get('LPOINTER'):  # maybe change it later
                return observer.failure(
                    InvalidSyntax(
                        self.token.position_start, 
                        self.token.position_end,
                        'assignment operator expected'
                    )
                )
            
            observer.register_next()
            self.next()

            expression = observer.register(self.expression())
            if observer.error: return observer

            return observer.success(VariableAssignmentNode(variable_name, expression))

        node = observer.register(
            self.binary_operation(
                self.compare_expression, (
                    (TokenTypes.get('KEYWORD'), 'and'),
                    (TokenTypes.get('KEYWORD'), 'or')
                )
            )
        )
        if observer.error: 
            return observer.failure(
                InvalidSyntax(
                    self.token.position_start, 
                    self.token.position_end,
                    'int, float, keyword, identifier or operator expected'                    
                )
            )
        
        return observer.success(node)

    def binary_operation(self, function, operators: tuple[str], function_second = None):
        if function_second == None:
            function_second = function

        observer = Result()

        left = observer.register(function())
        if observer.error: return observer

        while self.token.type in operators or (self.token.type, self.token.value) in operators:
            operator_token = self.token

            observer.register_next()
            self.next()
            
            right = observer.register(function_second())
            if observer.error: return observer
            
            left  = BinaryOperationNode(left, operator_token, right)
    
        return observer.success(left)
