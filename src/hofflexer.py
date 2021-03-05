from sly import Lexer

class HoffLexer(Lexer):
    tokens = { 
        ID, NUM, 
        ADD, SUB, MUL, DIV, MOD,
        LT, LE, EQ, NE, GE, GT,
        AND, OR, NOT,
        BIND,
        LP, RP,
        COMMA, COLON,
        LET, AND, IN, TEL,
        IF, THEN, ELSE, FI,
        FUN, CONST,
        MODULE, PUBLIC, PRIVATE,
    }

    ignore = ' \t\n'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'; NUM = r'[0-9]+([.][0-9]+)?' 
    
    ADD = r'\+'; SUB = r'-'; MUL = r'\*'; DIV = r'/'; MOD = r'%'
    
    LT = r'<'; LE = r'<='; EQ = r'=='; NE = r'!='; GE = r'>='; GT = r'>'

    #AND = r'\&\&'; 
    OR = r'\|\|'; NOT = r'!'
    
    BIND = r'='
    
    LP = r'\('; RP = r'\)'
    
    COMMA = r','; COLON = r':'

    ID['let'] = LET; ID['and'] = AND; ID['in'] = IN; ID['tel'] = TEL
    
    ID['if'] = IF; ID['then'] = THEN; ID['else'] = ELSE; ID['fi'] = FI
    
    ID['fun'] = FUN; ID['const'] = CONST
    
    ID['module'] = MODULE; ID['public'] = PUBLIC; ID['private'] = PRIVATE




