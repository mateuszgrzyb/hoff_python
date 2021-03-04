
from adt import adt, Case
from dataclasses import dataclass

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
class Decl:
    CONST: Case[str, Expr]
    FUN:   Case[str, list[str], Expr]


@dataclass
class Module:
    name: str
    decls: list[Decl]
