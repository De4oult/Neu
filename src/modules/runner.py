from core.lexer import Lexer

def execute(command: str) -> tuple[list[str], str]:
    lexer   = Lexer(command)
    tk, err = lexer.tokenize()

    return tk, err