from core.errors import RuntimeError

class Number:
    def __init__(self, value) -> None:
        self.value = value
        self.set_position()
    
    def set_position(self, start = None, end = None):
        self.position_start = start
        self.position_end   = end

        return self
    

    # Operations

    def addition(self, other) -> tuple:
        if isinstance(other, Number): return Number(self.value + other.value), None

    def subtraction(self, other) -> tuple: 
        if isinstance(other, Number): return Number(self.value - other.value), None
    
    def multiplication(self, other) -> tuple: 
        if isinstance(other, Number): return Number(self.value * other.value), None
    
    def division(self, other) -> tuple: 
        if isinstance(other, Number): 
            if other.value == 0: return None, RuntimeError(other.position_start, other.position_end, 'you can\'t divide by 0')
            return Number(self.value / other.value), None

    def __repr__(self) -> str:
        return str(self.value)