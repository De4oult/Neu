from modules.runner import execute
from colorama       import Fore, Style

def editor() -> None:
    line: int = 0 # current line
    while line < 1000:
        try:
            res, err = execute(input("{:03d} ~ ".format(line)))
            
            if err: print(err.as_string())
            else:   print(Fore.GREEN + f'{res}' + Style.RESET_ALL)
            
            line += 1

        except KeyboardInterrupt:
            exit()