


class NumberNode:
    def __init__(self, token) -> None:
        self.token = token

    def __repr__(self) -> str:
        return f'{self.token}'
    
class BinaryOperationNode:
    def __init__(self, left, operation, right) -> None:
        self.left      = left
        self.operation = operation
        self.right     = right

    def __repr__(self) -> str:
        return f'({self.left}, {self.operation}, {self.right})'
    
class UnaryOperationNode:
    def __init__(self, operation, node) -> None:
        self.operation = operation
        self.node      = node

    def __repr__(self) -> str:
        return f'({self.operation}, {self.node})'