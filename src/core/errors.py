

class Error:
    def __init__(self, name: str, info: str) -> None:
        self.name = name
        self.info = info

    def as_string(self):
        return f'{self.name}!!! ~> {self.info}'
    

