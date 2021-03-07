from src.hoffparser import HoffParser
from src.hofflexer import HoffLexer
from src.hoffcodegen import test, CodeGen


def main():
    lexer = HoffLexer()
    parser = HoffParser()
    cg = CodeGen()

    with open('main.ff', 'r') as f:
        # print(f.read())
        text = f.read()
        # print(list(lexer.tokenize(text)))
        tokens = lexer.tokenize(text)
        # print(parser.parse(tokens))
        tree = parser.parse(tokens)
        print(cg.generate(tree))
    
    # while True:
    #    try:
    #        text = input('hoff> ')
    #        tree = parser.parse(lexer.tokenize(text))
    #        print(tree)
    #    except (EOFError, KeyboardInterrupt):
    #        print('exit')
    #        break


if __name__ == '__main__':
    # test()
    main()
