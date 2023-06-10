from core.lexer import Lexer

def execute(command: str) -> None:
    lexer  = Lexer(command)
    tokens = lexer.tokenize()

    return tokens