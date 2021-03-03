from src.hoffparser import HoffParser
from src.hofflexer import HoffLexer
from src.hoffcodegen import test

if __name__ == '__main__':
    test()

def main():
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


