
from llvmlite import ir
from llvmlite.ir import Value

from .hoffast import Expr, Decl, Number, Module
from .hofflexer import HoffLexer
from .hoffparser import HoffParser

# compilation exception

class CompilationError(Exception):
    pass

class CodeGen:
    def __init__(self, module: Module) -> None:
        self.builder = ir.IRBuilder()
        self.module = ir.Module(module.name)
        self.values = dict()
        self.decls = module.decls

    def generate(self) -> str:
        for decl in self.decls:
            self.__gen_decl(decl)

        return str(self.module)


    # main gen
    def __gen_decl(self, decl: Decl):
        decl.match(
            Const = lambda n, e: self.__gen_bind(n, e),
            Fun   = lambda n, as_, e: self.__gen_fun(n, as_, e),
        )
    
    # decl gen
    def __gen_bind(self, name: str, expr: Expr):
        if name in self.values:
            raise CompilationError(f'Name {name} already exists')
        else:
           self.values[name] = self.__gen_expr(expr)

    def __gen_fun(self, name: str, args: list[str], body: Expr):

        function_type = ir.FunctionType(
            ir.DoubleType(), 
            [ir.DoubleType() for _ in args]
        )
        function = ir.Function(self.module, function_type, name)
        for name, arg in zip(args, function.args):
            arg.name = name
        
        block = function.append_basic_block(name='entry')
        self.builder.position_at_start(block)
       
        self.values.clear()
        for arg in function.args:
            self.values[arg.name] = arg
        
        result = self.__gen_expr(body)
       
        self.builder.ret(result)

    # expression gen
    def __gen_expr(self, expr: Expr):
        return expr.match(
            Var   = lambda n:          self.__gen_var(n),
            Num   = lambda i:          self.__gen_num(i),
            Binop = lambda e1, op, e2: self.__gen_binop(e1, op, e2),
            Unop  = lambda op, e:      self.__gen_unop(op, e),
            If    = lambda be, e1, e2: self.__gen_if(be, e1, e2),
            Let   = lambda bs, e:      self.__gen_let(bs, e),
            Call  = lambda n, as_:     self.__gen_call(n, as_),
        )

    def __gen_var(self, name: str) -> Value:
        if name in self.values:
            return self.values[name]
        else:
            raise CompilationError(
                f'No value with this name: {name}\n' +
                f'bound names: {self.values}'
            )

    def __gen_num(self, num: Number) -> Value:
        return ir.DoubleType()(num)

    def __gen_binop(self, expr1: Expr, op: str, expr2: Expr):
        l = self.__gen_expr(expr1)
        r = self.__gen_expr(expr2)
        return {
            '+':  lambda l, r: self.builder.fadd(l, r, 'addexpr'),
            '-':  lambda l, r: self.builder.fsub(l, r, 'subexpr'),
            '*':  lambda l, r: self.builder.fmul(l, r, 'mulexpr'),
            '/':  lambda l, r: self.builder.fdiv(l, r, 'divexpr'),
            '%':  lambda l, r: self.builder.frem(l, r, 'modexpr'),
            '<':  lambda l, r: self.builder.fcmp_ordered('<',  l, r, 'ltexpr'),
            '<=': lambda l, r: self.builder.fcmp_ordered('<=', l, r, 'leexpr'),
            '==': lambda l, r: self.builder.fcmp_ordered('==', l, r, 'eqexpr'),
            '!=': lambda l, r: self.builder.fcmp_ordered('!=', l, r, 'neexpr'),
            '>=': lambda l, r: self.builder.fcmp_ordered('>=', l, r, 'geexpr'),
            '>':  lambda l, r: self.builder.fcmp_ordered('>',  l, r, 'gtexpr'),
        }[op](l, r)

    def __gen_unop(self, op: str, expr: Expr):
        v = self.__gen_expr(expr)
        return {
            '-': lambda v: self.builder.fneg(v, 'negexpr'),
            '!': lambda v: self.builder.fneg(v, 'notexpr'),
        }[op](v)

    def __gen_if(self, bexpr: Expr, expr1: Expr, expr2: Expr):
        bvalue = self.__gen_expr(bexpr)
        function = self.builder.function

        then_bb = function.append_basic_block(name='then')
        else_bb = function.append_basic_block(name='else')
        result_bb = function.append_basic_block(name='result')


        

        phi = self.builder.phi(ir.DoubleType())
        phi.add_incoming(then_result, then_bb)
        phi.add_incoming(else_result, else_bb)

        self.builder.ret(phi)

    def __gen_let(self, binds: list[tuple[str, Expr]], expr: Expr):
        names = [name for name, _ in binds]
        self.values |= { n: self.__gen_expr(e) for n, e in binds }
        value = self.__gen_expr(expr)
        self.values = {k: v for k, v in self.values.items() if k not in names}
        return value
        
    def __gen_call(self, name: str, args: list[Expr]):
        try:
            function = self.module.get_global(name)
        except KeyError:
            raise CompilationError(
                f'No function with this name: {name}\n'
                f'declared functions: {self.module.functions}'
            )
        if len(function.args) != len(args):
            raise CompilationError(
                f'Wrong number of arguments\n' + 
                f'Args from caller: {args}\n' + 
                f'Args from function: {function.args}'
            )
        eval_args = [self.__gen_expr(arg) for arg in args]
        self.builder.call(name, eval_args, 'callexpr')

# test

def test():
    lexer = HoffLexer()
    parser = HoffParser()
    
    while True:
        try:
            text = input('hoff> ')
            tokens = lexer.tokenize(text)
            tree = parser.parse(tokens)
            self.__gen(tree)
            print(module)
        except EOFError:
            print()
            break

if __name__ == '__main__':
    test()

