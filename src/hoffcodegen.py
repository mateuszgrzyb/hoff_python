
from llvmlite import ir
from llvmlite.ir import Value

from .hoffast import Expr, Stmt, Number
from .hofflexer import HoffLexer
from .hoffparser import HoffParser

# compilation exception

class CompilationError(Exception):
    pass

# globals used for codegen

builder = ir.IRBuilder()
module = ir.Module('main')
values = dict()

# main codegen

def codegen(stmt: Stmt):
    stmt.match(
        Bind  = lambda n, e: codegen_bind(n, e),
        Fun   = lambda n, as_, e: codegen_fun(n, as_, e),
    )

# statement codegen

def codegen_expr(expr: Expr):
    return expr.match(
        Var   = lambda n: codegen_var(n),
        Num   = lambda i: codegen_num(i),
        Binop = lambda e1, op, e2: codegen_binop(e1, op, e2),
        Unop  = lambda op, e: codegen_unop(op, e),
        If    = lambda b, e1, e2: codegen_if(be, e1, e2),
        Let   = lambda bs, e: codegen_let(bs, e),
        Call  = lambda n, as_: codegen_call(n, as_),
    )

def codegen_bind(name: str, expr: Expr):
    if name in values:
        raise CompilationError(f'Name {name} already exists')
    else:
        values[name] = codegen_expr(expr)

def codegen_fun(name: str, args: list[str], body: Expr):
    function_type = ir.FunctionType(
        ir.DoubleType(), 
        [ir.DoubleType() for _ in args]
    )
    function = ir.Function(module, function_type, name)
    
    block = function.append_basic_block(name='entry')
    builder.position_at_start(block)
    result = codegen_expr(body)
    builder.ret(result)

# expression codegen

def codegen_var(name: str) -> Value:
    if name in values:
        return values[name]
    else:
        raise CompilationError(
            f'No value with this name: {name}\nbound names: {values}'
        )

def codegen_num(num: Number) -> Value:
    return ir.DoubleType()(num)

def codegen_binop(expr1: Expr, op: str, expr2: Expr):
    l = codegen_expr(expr1)
    r = codegen_expr(expr2)
    return {
        '+': lambda l, r: builder.fadd(l, r, 'addexpr'),
        '-': lambda l, r: builder.fsub(l, r, 'addexpr'),
        '*': lambda l, r: builder.fmul(l, r, 'addexpr'),
        '/': lambda l, r: builder.fdiv(l, r, 'addexpr'),
    }[op](expr1, expr2)

def codegen_unop(op: str, expr: Expr):
    v = codegen_expr(expr)
    return builder.fneg(v, 'negexpr')

def codegen_if(expr1: Expr, expr2: Expr, expr3: Expr):
    pass

def codegen_let(binds: list[tuple[str, Expr]], expr: Expr):
    pass

def codegen_call(name: str, args: list[Expr]):
    try:
        function = module.get_global(name)
    except KeyError:
        raise CompilationError(
            'No function with this name: {name}\ndeclared functions: {module.functions}'
        )
    if len(function.args) != len(args):
        raise CompilationError(
            f'Wrong number of arguments\nArgs from caller: {args}\nArgs from function: {function.args}'
        )
    eval_args = [codegen_expr(arg) for arg in args]
    builder.call(name, eval_args, 'callexpr')

# test

def test():
    lexer = HoffLexer()
    parser = HoffParser()
    
    while True:
        try:
            text = input('hoff> ')
            tokens = lexer.tokenize(text)
            tree = parser.parse(tokens)
            codegen(tree)
            print(module)
        except EOFError:
            print()
            break

if __name__ == '__main__':
    test()

