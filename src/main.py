from lark import Lark

grammer = ""

parser = Lark(grammer, parser='lalr', debug=True)


def main():
    return 0


if __name__ == "__main__":
    main()