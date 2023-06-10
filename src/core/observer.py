class Result:
    def __init__(self) -> None:
        self.error = None
        self.node  = None

    def register(self, result):
        if isinstance(result, Result):
            if result.error: self.error = result.error
            return result.node

        return result

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
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