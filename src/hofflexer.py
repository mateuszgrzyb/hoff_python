from sly import Lexer

class HoffLexer(Lexer):
    tokens = { 
        ID, NUM, 
        ADD, SUB, MUL, DIV,
        BIND,
        LP, RP,
        COMMA,
        LET, AND, IN, TEL,
        IF, THEN, ELSE, FI,
        FUN, BODY,
    }

    ignore = ' \t'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NUM = r'[0-9]+([.][0-9]+)?' 
    ADD = r'\+'; SUB = r'-'
    MUL = r'\*'; DIV = r'/'
    BIND = r'='
    BODY = r':'
    LP = r'\('; RP = r'\)'
    COMMA = r','

    ID['let'] = LET; ID['and'] = AND; ID['in'] = IN; ID['tel'] = TEL
    ID['if'] = IF; ID['then'] = THEN; ID['else'] = ELSE; ID['fi'] = FI
    ID['fun'] = FUN



