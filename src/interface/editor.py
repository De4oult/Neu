from modules.runner import execute
from colorama       import Fore, Style

def editor() -> None:
    line: int = -1 # current line
    while line < 1000:
        try:
            line += 1
            code     = input('{:03d} ~ '.format(line))
            if code.strip() == '': continue

            res, err = execute('<interpreter>', code)
            
            if err:   print(err.as_string())
            elif res: 
                if len(res.elements) == 1: print(Fore.GREEN + repr(res.elements[0]) + Style.RESET_ALL)
                else:                      print(Fore.GREEN + repr(res)             + Style.RESET_ALL)

        except KeyboardInterrupt:
            exit()