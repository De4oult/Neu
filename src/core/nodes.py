


class NumberNode:
    def __init__(self, token) -> None:
        self.token = token

        self.position_start = self.token.position_start
        self.position_end   = self.token.position_end

    def __repr__(self) -> str:
        return f'{self.token}'

class VariableAccessNode:
    def __init__(self, variable_name) -> None:
        self.variable_name = variable_name

        self.position_start = self.variable_name.position_start
        self.position_end   = self.variable_name.position_end

class VariableAssignmentNode:
    def __init__(self, variable_name, value) -> None:
        self.variable_name = variable_name
        self.value         = value

        self.position_start = self.variable_name.position_start
        self.position_end   = self.value.position_end

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
    
class IfNode:
    def __init__(self, cases, else_case) -> None:
        self.cases     = cases
        self.else_case = else_case

        self.position_start = self.cases[0][0].position_start
        self.position_end   = (self.else_case or self.cases[len(self.cases) - 1][0]).position_end