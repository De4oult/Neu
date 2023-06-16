from core.types       import Number, BuiltInFunction
from core.interpreter import Interpreter
from core.context     import Context
from core.parser      import Parser
from core.lexer       import Lexer
from core.table       import Table

table = Table()
# numbers
table.set('null',  Number.null)
table.set('true',  Number.true)
table.set('false', Number.false)

# functions
table.set('disp',     BuiltInFunction.disp)
table.set('displine', BuiltInFunction.displine)
table.set('read',     BuiltInFunction.read)
table.set('clear',    BuiltInFunction.clear)
table.set('typeof',   BuiltInFunction.typeof)
table.set('append',   BuiltInFunction.append)
table.set('pop',      BuiltInFunction.pop)
table.set('wait',     BuiltInFunction.wait)
table.set('length',   BuiltInFunction.length)

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

    #print(tokens)

    if ast.error: return None, ast.error

    interpreter = Interpreter()
    context = Context('<program>')
    context.table = table
    
    result  = interpreter.visit(ast.node, context)

    return result.value, result.error