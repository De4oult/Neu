from core.interpreter import Interpreter
from core.context     import Context
from core.parser      import Parser
from core.lexer       import Lexer

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

    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>') 
    result  = interpreter.visit(ast.node, context)

    return result.value, result.error