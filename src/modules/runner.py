from core.parser import Parser
from core.lexer  import Lexer

def execute(filename: str, content: str) -> tuple[list[str], str]:
    # Tokenizing
    lexer = Lexer(filename, content)
    
    (
        tokens, 
        error
    ) = lexer.tokenize()
    
    if error: return None, error

    # AST Generation
    parser = Parser(tokens)
    ast    = parser.parse()

    return ast, None