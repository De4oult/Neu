from modules.runner import execute
from colorama       import Fore, Style

def editor() -> None:
    line: int = 0 # current line
    while line < 1000:
        try:
            res, err = execute('<interpreter>', input("{:03d} ~ ".format(line)))
            
            if err:   print(err.as_string())
            elif res: 
                if len(res.elements) == 1: print(Fore.GREEN + repr(res.elements[0]) + Style.RESET_ALL)
                else:                      print(Fore.GREEN + repr(res)             + Style.RESET_ALL)
            
            line += 1

        except KeyboardInterrupt:
            exit()