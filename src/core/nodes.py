


class NumberNode:
    def __init__(self, token) -> None:
        self.token = token

        self.position_start = self.token.position_start
        self.position_end   = self.token.position_end


    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinaryOperationNode:
    def __init__(self, left, operation, right) -> None:
        self.left      = left
        self.operation = operation
        self.right     = right

        self.position_start = self.left.position_start
        self.position_end   = self.right.position_end

    def __repr__(self) -> str:
        return f'({self.left}, {self.operation}, {self.right})'
    
class UnaryOperationNode:
    def __init__(self, operation, node) -> None:
        self.operation = operation
        self.node      = node

        self.position_start = self.operation.position_start
        self.position_end   = node.position_end

    def __repr__(self) -> str:
        return f'({self.operation}, {self.node})'