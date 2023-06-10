from core.tokens import TokenTypes
from core.types  import Number

class Interpreter:
    def visit(self, node):
        method = getattr(
            self, 
            f'visit_{type(node).__name__}', 
            self.no_visit
        )
       
        return method(node)
    
    def no_visit(self, node):
        raise Exception(f'visit_{type(node).__name__} method is not defined')
    
    def visit_NumberNode(self, node):
        return Number(node.token.value).set_position(node.position_start, node.position_end)

    def visit_BinaryOperationNode(self, node):
        left  = self.visit(node.left)
        right = self.visit(node.right)

        if   node.operation.type == TokenTypes.get('PLUS'):  result = left.addition(right)
        elif node.operation.type == TokenTypes.get('MINUS'): result = left.subtraction(right)
        elif node.operation.type == TokenTypes.get('STAR'):  result = left.multiplication(right)
        elif node.operation.type == TokenTypes.get('SLASH'): result = left.division(right)

        return result.set_position(
            node.position_start, 
            node.position_end
        )

    def visit_UnaryOperationNode(self, node):
        number = self.visit(node.node)

        if node.operation.type == TokenTypes.get('MINUS'): number = number.multiplication(Number(-1))

        return number.set_position(
            node.position_start, 
            node.position_end
        )