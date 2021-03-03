
from adt import adt, Case

Number = float

@adt
class Expr:
    Var: Case[str]
    Num: Case[Number]
    BinOp: Case['Expr', str, 'Expr']
    UnOp: Case[str, 'Expr']
    If: Case['Expr', 'Expr', 'Expr']
    Let: Case[list[tuple[str, 'Expr']], 'Expr']
    Call: Case[str, list['Expr']]


@adt
class Stmt:
    Eval: Case[Expr]
    Bind: Case[str, Expr]
    Fun: Case[str, list[str], Expr]
