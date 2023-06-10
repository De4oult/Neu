from colorama import Fore, Style

class Error:
    def __init__(self, name: str, info: str) -> None:
        self.name = name
        self.info = info

    def as_string(self):
        return Fore.RED + f'{self.name} -> {self.info}' + Style.RESET_ALL # change it later
    

class UndefinedToken(Error):
    def __init__(self, info: str) -> None:
        super().__init__('Undefined Token', info)