
from adt import adt, Case

Number = float

@adt
class Expr:
    VAR:   Case[str]
    NUM:   Case[Number]
    BINOP: Case['Expr', str, 'Expr']
    UNOP:  Case[str, 'Expr']
    IF:    Case['Expr', 'Expr', 'Expr']
    LET:   Case[list[tuple[str, 'Expr']], 'Expr']
    CALL:  Case[str, list['Expr']]


@adt
class Stmt:
    BIND: Case[str, Expr]
    FUN:  Case[str, list[str], Expr]
