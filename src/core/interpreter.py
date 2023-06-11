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

        if   node.operation.type == TokenTypes.get('PLUS'):  result, error = left.addition(right)
        elif node.operation.type == TokenTypes.get('MINUS'): result, error = left.subtraction(right)
        elif node.operation.type == TokenTypes.get('STAR'):  result, error = left.multiplication(right)
        elif node.operation.type == TokenTypes.get('SLASH'): result, error = left.division(right)
        elif node.operation.type == TokenTypes.get('POW'):   result, error = left.exponentiation(right)

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

        if node.operation.type == TokenTypes.get('MINUS'): number, error = number.multiplication(Number(-1))

        if error: return observer.failure(error)
        
        return observer.success(number.set_position(
                node.position_start, 
                node.position_end
            )
        )
    