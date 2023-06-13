from core.errors import RuntimeError

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
    
