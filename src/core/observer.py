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
        self.reset()

    def reset(self):
        self.value         = None
        self.error         = None
        self.return_value  = None
        self.loop_continue = False
        self.loop_break    = False

    def register(self, result):
        if result.error: self.error = result.error
        self.return_value  = result.return_value
        self.loop_continue = result.loop_continue
        self.loop_break    = result.loop_break
        
        return result.value

    def success(self, value):
        self.reset()
        self.value = value
        
        return self

    def success_return(self, value):
        self.reset()
        self.return_value = value
        
        return self
    
    def success_continue(self):
        self.reset()
        self.loop_continue = True
        
        return self
    
    def success_break(self):
        self.reset()
        self.loop_break = True

        return self

    def failure(self, error):
        self.reset()
        self.error = error
        
        return self
    
    def should_return(self):
        return (
            self.error or
            self.return_value or
            self.loop_continue or
            self.loop_break
        )