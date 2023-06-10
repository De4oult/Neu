from colorama import Fore, Style

class Position:
    def __init__(self, index: int, line: int, column: int, filename: str, file_text: str) -> None:
        self.index     = index
        self.line      = line
        self.column    = column
        self.filename  = filename
        self.file_text = file_text

    def next(self, char: int):
        self.index  += 1
        self.column += 1

        if char == '\n':
            self.line  += 1
            self.column = 0

        return self
    
    def copy(self):
        return Position(
            self.index,
            self.line,
            self.column,
            self.filename,
            self.file_text
        )

class Error:
    def __init__(self, start: int, end: int, name: str, info: str) -> None:
        self.position_start = start
        self.position_end   = end
        self.name           = name
        self.info           = info

    def as_string(self):
        return Fore.RED + f'{self.name} -> {self.info} \nFile `{self.position_start.filename}` on line {self.position_start.line + 1}' + Style.RESET_ALL # change it later
    

class UndefinedToken(Error):
    def __init__(self, start: int, end: int, info: str) -> None:
        super().__init__(start, end, 'Undefined Token', info)

class InvalidSyntax(Error):
    def __init__(self, start: int, end: int, info: str) -> None:
        super().__init__(start, end, 'Invalid Syntax', info)