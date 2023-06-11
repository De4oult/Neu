from core.observer import RuntimeResult
from core.tokens   import TokenTypes
from core.errors   import RuntimeError
from core.types    import Number

class Interpreter:
    def visit(self, node, context):
        method = getattr(
            self, 
            f'visit_{type(node).__name__}', 
            self.no_visit
        )
       
        return method(node, context)
    
    def no_visit(self, node, context):
        raise Exception(f'visit_{type(node).__name__} method is not defined')
    
    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(Number(node.token.value).set_context(context).set_position(node.position_start, node.position_end))

    def visit_VariableAccessNode(self, node, context):
        observer = RuntimeResult()

        variable_name = node.variable_name.value
        value         = context.table.get(variable_name)

        if not value:
            return observer.failure(
                RuntimeError(
                    node.position_start, 
                    node.position_end,
                    f'`{variable_name}` is not defined',
                    context
                )
            )
        
        value = value.copy().set_position(node.position_start, node.position_end)
        return observer.success(value)

    def visit_VariableAssignmentNode(self, node, context):
        observer = RuntimeResult()
        
        variable_name = node.variable_name.value
        value         = observer.register(self.visit(node.value, context))
        if observer.error: return observer

        context.table.set(variable_name, value)
        return observer.success(value)

    def visit_BinaryOperationNode(self, node, context):
        observer = RuntimeResult()

        left  = observer.register(self.visit(node.left, context))
        if observer.error: return observer

        right = observer.register(self.visit(node.right, context))
        if observer.error: return observer

        # MATH
        if   node.operation.type == TokenTypes.get('PLUS'):  result, error = left.addition(right)
        elif node.operation.type == TokenTypes.get('MINUS'): result, error = left.subtraction(right)
        elif node.operation.type == TokenTypes.get('STAR'):  result, error = left.multiplication(right)
        elif node.operation.type == TokenTypes.get('SLASH'): result, error = left.division(right)
        elif node.operation.type == TokenTypes.get('POW'):   result, error = left.exponentiation(right)
        # LOGICAL
        elif node.operation.type == TokenTypes.get('EE'):              result, error = left.comparison_eq(right)
        elif node.operation.type == TokenTypes.get('NE'):              result, error = left.comparison_ne(right)
        elif node.operation.type == TokenTypes.get('LT'):              result, error = left.comparison_lt(right)
        elif node.operation.type == TokenTypes.get('GT'):              result, error = left.comparison_gt(right)
        elif node.operation.type == TokenTypes.get('LTE'):             result, error = left.comparison_lte(right)
        elif node.operation.type == TokenTypes.get('GTE'):             result, error = left.comparison_gte(right)
        elif node.operation.matches(TokenTypes.get('KEYWORD'), 'and'): result, error = left.comparison_and(right)
        elif node.operation.matches(TokenTypes.get('KEYWORD'), 'or' ): result, error = left.comparison_or(right)


        if error: return observer.failure(error)
            
        return observer.success(result.set_position(
                node.position_start, 
                node.position_end
            )
        )

    def visit_UnaryOperationNode(self, node, context):
        observer = RuntimeResult()

        number = observer.register(self.visit(node.node, context))
        if observer.error: return observer

        error = None

        if   node.operation.type == TokenTypes.get('MINUS'):           number, error = number.multiplication(Number(-1))
        elif node.operation.type == TokenTypes.get('INC'):             number, error = number.increment()
        elif node.operation.type == TokenTypes.get('DEC'):             number, error = number.decrement()
        elif node.operation.matches(TokenTypes.get('KEYWORD'), 'not'): number, error = number.negation()

        if error: return observer.failure(error)
        
        return observer.success(number.set_position(
                node.position_start, 
                node.position_end
            )
        )
    
    def visit_IfNode(self, node, context):
        observer = RuntimeResult()

        for condition, expression in node.cases:
            condition = observer.register(self.visit(condition, context))
            if observer.error: return observer

            if condition.is_true():
                expression = observer.register(self.visit(expression, context))
                if observer.error: return observer

                return observer.success(expression)
            
        if node.else_case:
            else_value = observer.register(self.visit(node.else_case, context))
            if observer.error: return observer

            return observer.success(else_value)
    
        return observer.success(None)