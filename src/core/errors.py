from colorama import Fore, Style

class Position:
    def __init__(self, index: int, line: int, column: int, filename: str, file_text: str) -> None:
        self.index     = index
        self.line      = line
        self.column    = column
        self.filename  = filename
        self.file_text = file_text

    def next(self, char: int = None):
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
        return Fore.RED + f'{self.name} -> {self.info} \nFile `{self.position_start.filename}` on line {self.position_start.line + 1}\n' + Style.RESET_ALL # change it later
    

class UndefinedToken(Error):
    def __init__(self, start: int, end: int, info: str) -> None:
        super().__init__(start, end, 'Undefined Token', info)

class InvalidSyntax(Error):
    def __init__(self, start: int, end: int, info: str) -> None:
        super().__init__(start, end, 'Invalid Syntax', info)

class RuntimeError(Error):
    def __init__(self, start: int, end: int, info: str, context: str) -> None:
        super().__init__(start, end, 'Runtime Error', info)
        
        self.context = context

    def traceback(self):
        result   = ''
        position = self.position_start
        context  = self.context

        while context:
            result   = f'   File `{position.filename}` on line {position.line + 1} in {context.display}\n' + result
            position = context.parent_entry_position
            context  = context.parent

        return 'Traceback: \n' + result

    def as_string(self) -> str:
        return Fore.RED + f'{self.traceback()}{self.name} -> {self.info}\n' + Style.RESET_ALL  