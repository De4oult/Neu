from core.errors import RuntimeError

class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_position()
        self.set_context()
    
    def set_position(self, start = None, end = None):
        self.position_start = start
        self.position_end   = end

        return self
    
    def set_context(self, context = None):
        self.context = context
        return self

    # Math Operations
    def addition(self, other) -> tuple:
        if isinstance(other, Number): return Number(self.value + other.value).set_context(self.context), None

    def subtraction(self, other) -> tuple: 
        if isinstance(other, Number): return Number(self.value - other.value).set_context(self.context), None
    
    def multiplication(self, other) -> tuple: 
        if isinstance(other, Number): return Number(self.value * other.value).set_context(self.context), None
    
    def division(self, other) -> tuple: 
        if isinstance(other, Number): 
            if other.value == 0: return None, RuntimeError(other.position_start, other.position_end, 'you can\'t divide by 0', self.context)
            return Number(self.value / other.value).set_context(self.context), None

    def exponentiation(self, other) -> tuple:
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    # Logical Operations
    def comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def comparison_and(self, other):
        if isinstance(other, Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def comparison_or(self, other):
        if isinstance(other, Number):
            return Number(int(self.value or other.value)).set_context(self.context), None

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
    