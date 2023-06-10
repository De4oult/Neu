from modules.runner import execute

def editor() -> None:
    line: int = 0 # current line
    while line < 1000:
        try:
            print(execute(input("{:03d} ~ ".format(line))))
            line += 1

        except KeyboardInterrupt:
            exit()