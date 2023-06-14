class Result:
    def __init__(self) -> None:
        self.error         = None
        self.node          = None
        self.last_next     = 0
        self.next_count    = 0
        self.reverse_count = 0

    def register_next(self):
        self.last_next   = 1
        self.next_count += 1

    def register(self, result):
        self.last_next   = self.next_count
        self.next_count += result.next_count
        
        if result.error: self.error = result.error
        
        return result.node

    def try_register(self, result):
        if result.error:
            self.reverse_count = result.next_count
            return None
        
        return self.register(result)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.next_count == 0:
            self.error = error
        return self
    

class RuntimeResult:
    def __init__(self) -> None:
        self.value = None
        self.error = None

    def register(self, result):
        if result.error: self.error = result.error
        return result.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self