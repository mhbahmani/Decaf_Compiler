from lark import Lark
# from CGEN import cgen
from parseTree import build_parser_tree
import sys

grammer = r"""
start : program

nothing :

program : decl+

decl : variabledecl
        | functiondecl
        | classdecl
        | interfacedecl

variabledecls : variabledecl+

variabledecl : variable ";"

variable : type T_ID

type : T_INT (array)+
        | T_DOUBLE (array)+
        | T_BOOL (array)+
        | T_STRING (array)+
        | T_ID  (array)+


array: "[]"

functiondecl : type T_ID "(" formals ")" stmtblock
        | T_VOID T_ID "(" formals ")" stmtblock


formals : (variable formalscontinue)?

formalscontinue : ("," variable)*

classdecl : T_CLASS T_ID extends implements  "{" field* "}"

extends : T_EXTENDS T_ID
        | nothing

implements : T_IMPLEMENTS T_ID ids
        | nothing

ids : ("," T_ID)*

fields : field*

field : accessmode variabledecl
        | accessmode functiondecl

accessmode : T_PRIVATE
        | T_PROTECTED
        | T_PUBLIC
        | nothing

interfacedecl : T_INTERFACE T_ID "{" prototype* "}"

prototypes : prototype*

prototype : type T_ID "(" formals ")" ";"
        | T_VOID T_ID "(" formals ")" ";"


stmtblock : "{" variabledecls stmt* "}"

stmt : nullexpr ";"
        | ifstmt
        | whilestmt
        | forstmt
        | breakstmt
        | continuestmt
        | returnstmt
        | printstmt
        | stmtblock

stmts : stmt*


ifstmt : T_IF "(" expr ")" stmt ifextra

ifextra : (T_ELSE stmt)?

whilestmt : T_WHILE "(" expr ")" stmt

forstmt : T_FOR "(" nullexpr ";" expr ";" nullexpr ")" stmt

returnstmt : T_RETURN nullexpr ";"

breakstmt : T_BREAK ";"

continuestmt : T_CONTINUE ";"

printstmt : T_PRINT "(" expr exprs ")" ";"

expr : lvalue
        | lvalue "=" expr
        | T_ID
        | T_ID "=" expr
        | constant
        | T_THIS
        | call
        | "(" expr ")"
        | expr "+" expr
        | expr "-" expr
        | expr "*" expr
        | expr "/" expr
        | expr "%" expr
        | expr "<" expr
        | expr  T_LESS_THAN_EQUAL expr
        | expr ">" expr
        | expr T_GREATER_THAN_EQUAL expr
        | expr T_EQUAL expr
        | expr T_NOT_EQUAL expr
        | expr T_AND expr
        | expr T_OR expr
        | "-" expr
        | "!" expr
        | T_READINTEGER "(" ")"
        | T_READLINE "(" ")"
        | T_NEW T_ID
        | T_NEWARRAY "(" expr "," type ")"
        | T_NEWARRAY "(" expr "," T_ID ")"
        | T_ITOD "(" expr ")"
        | T_DITOI "(" expr ")"
        | T_ITOB "(" expr ")"
        | T_BTOI "(" expr ")"

nullexpr : (expr)?

exprs : ("," expr)*

lvalue : expr "." T_ID
        | expr "[" expr "]"

call : T_ID "(" actuals ")"
        | expr "." T_ID "(" actuals ")"

actuals : (expr exprs)?

constant : T_INT_CONSTANT
        | T_DOUBLE_CONSTANT
        | bool_constant
        | T_STRING_CONSTANT
        | T_NULL

bool_constant : T_TRUE
	    | T_FALSE

T_VOID : "void"
T_INT : "int"
T_DOUBLE : "double"
T_BOOL : "bool"
T_STRING : "string"
T_CLASS : "class"
T_INTERFACE : "interface"
T_NULL : "null"
T_THIS : "this"
T_EXTENDS : "extends"
T_IMPLEMENTS : "implemnts"
T_FOR : "for"
T_WHILE : "while"
T_IF : "if"
T_ELSE : "else"
T_RETURN : "return"
T_BREAK : "break"
T_CONTINUE : "continue"
T_NEW : "new"
T_NEWARRAY : "NewArray"
T_PRINT : "Print"
T_READINTEGER : "ReadInteger"
T_READLINE : "ReadLine"
T_DITOI : "ditol"
T_ITOD : "itod"
T_BTOI : "btoi"
T_ITOB : "itob"
T_PRIVATE : "private"
T_PROTECTED : "protected"
T_PUBLIC : "public"
T_TRUE : "true"
T_FALSE : "false"
T_AND : "&&"
T_OR : "\|\|"
T_EQUAL : "=="
T_NOT_EQUAL : "!="
T_LESS_THAN_EQUAL : "<="
T_GREATER_THAN_EQUAL : ">="
T_ID : /[a-zA-Z]([a-zA-Z0-9]|\_)*/
T_STRING_CONSTANT : /\d+\.\d*[E,e]\+?\d+/ | /\d+\.\d*/
T_INT_CONSTANT : /0[x|X][\da-fA-F]*/ | /\d+/
T_DOUBLE_CONSTANT : /"[^"^\n]*"/
WHITE_SPACE : /[ \r\f\s\t\n]/
SINGLE_LINE_COMMENT : /\/\/[^\n]*/
MULTI_LINE_COMMENT : /\/\* [.\n]* \*\//
%import common.WS -> WHITESPACE
%ignore WHITE_SPACE
%ignore SINGLE_LINE_COMMENT
%ignore MULTI_LINE_COMMENT

"""

parser = Lark(grammer, parser="lalr", debug=True)


def main(argv):
    _input = ""
    _output = ""
    if (len(argv) % 2 != 0):
        sys.stderr.write("invalid command, should be like: main.py -i <input file> -o <output file>\n")
        sys.exit(2)
    for i in range(0, len(argv), 2):
        if (argv[i] == "-i" or argv[i] == "--ifile"):
            _input = argv[i + 1]
        elif (argv[i] == "-o" or argv[i] == "--ofile"):
            _output = argv[i + 1]

    if _input == "":
        sys.stderr.write("no input file provided!\n")
        sys.exit(2)
    if _output == "":
        sys.stderr.write("no output file provided!\n")
        sys.exit(2)
    
    with open("tests/" + _input, "r") as input_file:
        code = input_file.read()
        lark_tree = parser.parse(code)
        parseTree = build_parser_tree(lark_tree)

    with open("out/" + _output, "w") as output_file:
        sys.stdout = output_file
        cgen(parseTree)
        sys.stdout.close()


if __name__ == "__main__":
    main(sys.argv[1:])
