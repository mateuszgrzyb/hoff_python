from sly import Parser
from .hofflexer import HoffLexer
from .hoffast import Expr, Stmt
from math import nan

class HoffParser(Parser):
    def __init__(self):
        self.variables = dict()

    tokens = HoffLexer.tokens
    start = 'stmt'

    precedence = [
        ('left', ADD, SUB),
        ('left', MUL, DIV),
        ('right', NEG),
    ]

    @_('expr')
    def stmt(self, p):
        return Stmt.Eval(p.expr)

    @_('ID BIND expr')
    def stmt(self, p):
        return Stmt.Bind(p.ID, p.expr)

    @_('FUN ID LP ID { COMMA ID } RP BODY expr')
    def stmt(self, p):
        args = [p.ID1] + [i[1] for i in p[4]]
        return Stmt.Fun(p.ID0, args, p.expr)

    @_('IF expr THEN expr ELSE expr FI')
    def expr(self, p):
        return Expr.If(p.expr0, p.expr1, p.expr2)

    @_('LET ID BIND expr { AND ID BIND expr } IN expr TEL')
    def expr(self, p):
        bindings = [(p.ID0, p.expr0)] + \
                   [(b[1], b[3]) for b in p[4]]
        return Expr.Let(bindings, p.expr2)

    @_('ID LP expr { COMMA expr } RP')
    def expr(self, p):
        args = [p.expr0] + [e[1] for e in p[3]]
        return Expr.Call(p.ID, args)

    @_('expr ADD expr',
       'expr SUB expr',
       'expr MUL expr',
       'expr DIV expr')
    def expr(self, p):
        return Expr.BinOp(p.expr0, p[1], p.expr1)

    @_('SUB expr %prec NEG')
    def expr(self, p):
        return Expr.UnOp(p.SUB, p.expr)
    
    @_('NUM')
    def expr(self, p):
        return Expr.Num(p.NUM)

    @_('LP expr RP')
    def expr(self, p):
        return p.expr

    @_('ID')
    def expr(self, p):
        return Expr.Var(p.ID)

