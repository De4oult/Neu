


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

class ForNode:
    def __init__(self, variable_name, start_value, end_value, step_value, body) -> None:
        self.variable_name = variable_name
        self.start_value   = start_value
        self.end_value     = end_value
        self.step_value    = step_value
        self.body          = body

        self.position_start = self.variable_name.position_start
        self.position_end   = self.body.position_end

class LoopNode:
    def __init__(self, condition, body) -> None:
        self.condition = condition
        self.body      = body

        self.position_start = self.condition.position_start
        self.position_end   = self.body.position_end 

class FunctionDefinitionNode:
    def __init__(self, variable_name, arguments_names, body) -> None:
        self.variable_name   = variable_name
        self.arguments_names = arguments_names
        self.body            = body

        if self.variable_name:
            self.position_start = self.variable_name.position_start
        
        elif len(self.arguments_names) > 0:
            self.position_start = self.arguments_names[0].position_start
        
        else:
            self.position_start = self.body.position_start

        self.position_end = self.body.position_end

class CallNode:
    def __init__(self, node, arguments_names) -> None:
        self.node            = node
        self.arguments_names = arguments_names

        self.position_start = self.node.position_start

        if len(self.arguments_names) > 0:
            self.position_end = self.arguments_names[len(self.arguments_names) - 1].position_end
        else:
            self.position_end = self.node.position_end