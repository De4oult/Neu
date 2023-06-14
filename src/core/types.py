from core.observer    import RuntimeResult
from core.errors      import RuntimeError
from core.context     import Context
from core.table       import Table

import os

class Value:
    def __init__(self) -> None:
        self.set_position()
        self.set_context()

    def set_position(self, start = None, end = None):
        self.position_start = start
        self.position_end   = end

        return self
    
    def set_context(self, context = None):
        self.context = context

        return self
    
    def addition(self, other) -> tuple:
        return None, self.illegal_operation(other)

    def subtraction(self, other) -> tuple:
        return None, self.illegal_operation(other)
    
    def multiplication(self, other) -> tuple:
        return None, self.illegal_operation(other)
    
    def division(self, other) -> tuple:
        return None, self.illegal_operation(other)

    def exponentiation(self, other) -> tuple:
        return None, self.illegal_operation(other)

        # Logical Operations
    def comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def comparison_and(self, other):
        return None, self.illegal_operation(other)

    def comparison_or(self, other):
        return None, self.illegal_operation(other)
    
    def negation(self):
        return None, self.illegal_operation()

    def increment(self):
        return None, self.illegal_operation()

    def decrement(self):
        return None, self.illegal_operation()
    
    def push(self, other):
        return None, self.illegal_operation(other)
    
    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False
    
    def illegal_operation(self, other = None):
        if not other: other = self
        return RuntimeError(
            self.position_start,
            other.position_end,
            'Illegal operation',
            self.context
        )

class Number(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    # Math Operations
    def addition(self, other) -> tuple:
        if isinstance(other, Number): return Number(self.value + other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self.position_start, other.position_end)

    def subtraction(self, other) -> tuple: 
        if isinstance(other, Number): return Number(self.value - other.value).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)
    
    def multiplication(self, other) -> tuple: 
        if isinstance(other, Number): return Number(self.value * other.value).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)
    
    def division(self, other) -> tuple: 
        if isinstance(other, Number): 
            if other.value == 0: return None, RuntimeError(other.position_start, other.position_end, 'you can\'t divide by 0', self.context)
            return Number(self.value / other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self.position_start, other.position_end)

    def exponentiation(self, other) -> tuple:
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None
        
        return None, Value.illegal_operation(self.position_start, other.position_end)

    # Logical Operations
    def comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    def comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    def comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    def comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    def comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    def comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    def comparison_and(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    def comparison_or(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

        return None, Value.illegal_operation(self.position_start, other.position_end)

    # Unary
    def negation(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def increment(self):
        return Number(self.value + 1).set_context(self.context), None

    def decrement(self):
        return Number(self.value - 1).set_context(self.context), None
    
    # Service methods
    def copy(self):
        return Number(self.value).set_position(self.position_start, self.position_end).set_context(self.context)

    def is_true(self):
        return self.value != 0

    def __repr__(self) -> str:
        return str(self.value)
    
Number.null  = Number(0)
Number.false = Number(0)
Number.true  = Number(1)

class String(Value):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

    def addition(self, other) -> tuple:
        if isinstance(other, String): return String(self.value + other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)
    
    def multiplication(self, other) -> tuple:
        if isinstance(other, Number): return String(self.value * other.value).set_context(self.context), None
        return None, Value.illegal_operation(self, other)
    
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        return String(self.value).set_position(self.position_start, self.position_end).set_context(self.context)
    
    def __repr__(self) -> str:
        return f'"{self.value}"'

class List(Value):
    def __init__(self, elements) -> None:
        super().__init__()
        self.elements = elements

    def addition(self, other) -> tuple:
        new_array = self.copy()
        if isinstance(other, List):
            for element in other.elements:
                new_array.elements.append(element)

            return new_array, None
        
        new_array.elements.append(other)
        
        return new_array, None
    
    def push(self, other) -> tuple:
        new_array = self.copy()
        new_array.elements.append(other)
        
        return new_array, None

    def copy(self):
        return List(self.elements).set_position(self.position_start, self.position_end).set_context(self.context)
    
    def __repr__(self) -> str:
        return f'[{", ".join([str(element) for element in self.elements])}]'

class BaseFunction(Value):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name or '<anonyomus>'

    def generate_context(self):
        context = Context(self.name, self.context, self.position_start)
        context.table = Table(context.parent.table)

        return context

    def check_arguments(self, arguments_names, arguments):
        observer = RuntimeResult()

        if len(arguments) != len(arguments_names):
            return observer.failure(
                RuntimeError(
                    self.position_start, 
                    self.position_end,
                    f'{len(arguments)} arguments passed, expected {len(self.arguments_names)}'
                )
            )
        
        return observer.success(None)
    
    def populate_arguments(self, arguments_names, arguments, context):
        for i in range(len(arguments)):
            argument_name  = arguments_names[i]
            argument_value = arguments[i]
                
            argument_value.set_context(context)
            context.table.set(argument_name, argument_value)

    def validate_arguments(self, arguments_names, arguments, context):
        observer = RuntimeResult()

        observer.register(self.check_arguments(arguments_names, arguments))
        if observer.error: return observer

        self.populate_arguments(arguments_names, arguments, context)

        return observer.success(None)


class Function(BaseFunction):
    def __init__(self, name, body, arguments_names, return_null) -> None:
        super().__init__(name)
        self.body            = body
        self.arguments_names = arguments_names
        self.return_null     = return_null

    def execute(self, arguments, interpreter):
        observer = RuntimeResult()

        context = self.generate_context()
        
        observer.register(self.validate_arguments(self.arguments_names, arguments, context))
        if observer.error: return observer

        value = observer.register(interpreter.visit(self.body, context))
        if observer.error: return observer

        return observer.success(Number.null if self.return_null else value)
    
    def copy(self):
        return Function(self.name, self.body, self.arguments_names, self.return_null).set_context(self.context).set_position(self.position_start, self.position_end)
    
    def __repr__(self) -> str:
        return f'<function {self.name}>'
    
class BuiltInFunction(BaseFunction):
    def __init__(self, name) -> None:
        super().__init__(name)

    def execute(self, arguments, interpreter = None):
        observer = RuntimeResult()

        context = self.generate_context()

        method = getattr(self, f'execute_{self.name}', self.no_visit)

        observer.register(self.validate_arguments(method.arguments_names, arguments, context))
        if observer.error: return observer

        return_value = observer.register(method(context))
        if observer.error: return observer

        return observer.success(return_value)
    
    def no_visit(self, node, context):
        raise Exception(f'execute_{self.name} method is not defined')
    
    def copy(self):
        return BuiltInFunction(self.name).set_context(self.context).set_position(self.position_start, self.position_end)
    
    def __repr__(self) -> str:
        return f'<built-in function {self.name}>'
    
    def execute_disp(self, context):
        print(str(context.table.get('value')), end = '')
        
        return RuntimeResult().success(Number.null)
    
    execute_disp.arguments_names = ['value']
    
    def execute_displine(self, context):
        print(str(context.table.get('value')))
        
        return RuntimeResult().success(Number.null)
    
    execute_displine.arguments_names = ['value']

    def execute_read(self, context):
        text = input()

        return RuntimeResult().success(String(text))
    
    execute_read.arguments_names = []

    def execute_clear(self, context):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RuntimeResult().success(Number.null)

    execute_clear.arguments_names = []

    def execute_typeof(self, context):
        return RuntimeResult().success(String(type(context.table.get('value'))))
    
    execute_typeof.arguments_names = ['value']

    def execute_append(self, context):
        array = context.table.get('list')
        value = context.table.get('value')

        if not isinstance(array, List):
            return RuntimeResult().failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    'first argument must be list',
                    context
                )
            )
        
        array.elements.append(value)

        return RuntimeResult().success(Number.null)

    execute_append.arguments_names = ['list', 'value']

    def execute_pop(self, context):
        array = context.table.get('list')
        index = context.table.get('index')

        if not isinstance(array, List):
            return RuntimeResult().failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    'first argument must be list',
                    context
                )
            )
        
        if not isinstance(index, Number):
            return RuntimeResult().failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    'second argument must be number',
                    context
                )
            )
        
        try:
            element = array.elements.pop(index.value)
        except:
            return RuntimeResult().failure(
                RuntimeError(
                    self.position_start,
                    self.position_end,
                    'element at this index could not be removed',
                    context
                )
            )

        return RuntimeResult().success(element)

    execute_pop.arguments_names = ['list', 'index']

BuiltInFunction.disp     = BuiltInFunction("disp")
BuiltInFunction.displine = BuiltInFunction("displine")
BuiltInFunction.read     = BuiltInFunction("read")
BuiltInFunction.clear    = BuiltInFunction("clear")
BuiltInFunction.typeof   = BuiltInFunction("typeof")
BuiltInFunction.append   = BuiltInFunction("append")
BuiltInFunction.pop      = BuiltInFunction("pop")