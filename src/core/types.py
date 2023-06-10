

class Number:
    def __init__(self, value) -> None:
        self.value = value
    
    def set_position(self, start = None, end = None):
        self.start = start
        self.end   = end

        return self
    

    # Operations

    def addition(self, other):
        if isinstance(other, Number): return Number(self.value + other.value)

    def subtraction(self, other): 
        if isinstance(other, Number): return Number(self.value - other.value)
    
    def multiplication(self, other): 
        if isinstance(other, Number): return Number(self.value * other.value)
    
    def division(self, other): 
        if isinstance(other, Number): return Number(self.value / other.value)

    def __repr__(self) -> str:
        return str(self.value)