from core.lexer import Lexer

def execute(filename: str, content: str) -> tuple[list[str], str]:
    lexer   = Lexer(filename, content)
    tk, err = lexer.tokenize()

    return tk, err