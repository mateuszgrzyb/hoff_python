
from llvmlite import ir
from .hoffast import Expr, Stmt, Number

# main codegen

def codegen(stmt: Stmt):
    return stmt.match(
        eval_ = lambda e: codegen_eval(e),
        bind  = lambda name e: codegen_bind(name, e),
        fun   = lambda name args e: codegen_fun(name, args, e),
    )

# statement codegen

def codegen_eval(expr: Expr):
    return expr.match(
        var   = lambda n: codegen_var(n),
        num   = lambda i: codegen_num(i),
        binop = lambda e1 op e2: codegen_binop(e1, op, e2),
        unop  = lambda op e: codegen_unop(op, e),
        if_   = lambda b e1 e2: codegen_if(be, e1, e2),
        let   = lambda bs e: codegen_let(bs, e),
        calli = lambda n as_: codegen_call(n, as_),
    )

def codegen_bind(name: str, expr: Expr):
    pass

def codegen_fun(name: str, args: list[str], expr: Expr):
    pass

# expression codegen

def codegen_var(name: str):
    pass

def codegen_num(num: Number):
    pass

def codegen_binop(expr1: Expr, op: str, expr2: Expr):
    return {
        '+': lambda e1 e2: codegen_add(e1, e2),
        '-': lambda e1 e2: codegen_sub(e1, e2),
        '*': lambda e1 e2: codegen_mul(e1, e2),
        '/': lambda e1 e2: codegen_div(e1, e2),
    }[op](expr1, expr2)

def codegen_unop(op: str, expr: Expr):
    pass

def codegen_if(expr1: Expr, expr2: Expr, expr3: Expr):
    pass

def codegen_let(binds: list[tuple[str, Expr]], expr: Expr):
    pass

def codegen_call(name: str, args: list[Expr]):
    pass

# binop codegen

def codegen_add(expr1: Expr, expr2: Expr):
    pass

def codegen_sub(expr1: Expr, expr2: Expr):
    pass

def codegen_mul(expr1: Expr, expr2: Expr):
    pass

def codegen_div(expr1: Expr, expr2: Expr):
    pass

