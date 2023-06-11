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

    # Operations

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

    def __repr__(self) -> str:
        return str(self.value)