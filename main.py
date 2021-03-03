from src.hoffparser import HoffParser
from src.hofflexer import HoffLexer

if __name__ == '__main__':
    lexer = HoffLexer()
    parser = HoffParser()

    while True:
        try:
            text = input('hoff> ')
            tree = parser.parse(lexer.tokenize(text))
            print(tree)
        except (EOFError, KeyboardInterrupt):
            print('exit')
            break


