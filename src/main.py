from lark import Lark
from CGEN import cgen
from table import emit
from parseTree import build_parser_tree
import sys
import os

grammar = """
start : program

program : (decl)+

decl : classdecl
        | functiondecl
        | variabledecl
        | interfacedecl

variabledecls : (variabledecl)+

variabledecl : variable ";"

variable : type T_ID

type : T_INT (array)*
        | T_DOUBLE (array)*
        | T_BOOL (array)*
        | T_STRING (array)*
        | T_ID (array)*

array : "[]"

functiondecl : type T_ID "(" formals ")" stmtblock
                | T_VOID T_ID "(" formals ")" stmtblock

formals : (variable formalscontinue)?

formalscontinue : ("," variable)*

classdecl : T_CLASS T_ID extends implements "{" field* "}"

extends : T_EXTENDS T_ID
        | nothing

implements : T_IMPLEMENTS T_ID ids
        | nothing

ids : ("," T_ID)*

field : accessmode variabledecl
        | accessmode functiondecl

accessmode : T_PRIVATE
        | T_PROTECTED
        | T_PUBLIC
        | nothing

interfacedecl : T_INTERFACE T_ID "{" prototypes "}"

prototypes : prototype*

prototype : type T_ID "(" formals ")" ";"
        | T_VOID T_ID "(" formals ")" ";"

stmtblock : "{" variabledecl* stmt* "}"

stmt : nullexpr ";"
        | ifstmt
        | whilestmt
        | forstmt
        | breakstmt
        | continuestmt
        | returnstmt
        | printstmt
        | stmtblock

nullexpr : expr | nothing

stmts : stmt*

forstmt : T_FOR "(" nullexpr ";" expr ";" nullexpr ")" stmt

ifstmt : T_IF "(" expr ")" stmt ifextra

ifextra : T_ELSE stmt 
        | nothing

nothing :  

whilestmt : T_WHILE "(" expr ")" stmt

returnstmt : T_RETURN nullexpr ";"

continuestmt : T_CONTINUE ";"

breakstmt : T_BREAK ";"

printstmt : T_PRINT "(" expr exprs ")" ";"

exprs : ("," expr)*

expr :  expr1
        | lvalue T_ASSIGN expr

expr1 : expr1 T_AND expr2
        | expr3

expr2 : expr2 T_OR expr3
        | expr3

expr3 : expr3 ( T_EQUAL | T_NOT_EQUAL ) expr4
        | expr4

expr4 : expr4 (T_LESS_THAN_EQUAL | T_GREATER_THAN_EQUAL | ">" | "<" ) expr5
        | expr5

expr5 : expr5 ( "*" | "/" | "%" ) expr6
        | expr6

expr6 : expr6 ( "-" | "+" ) expr7
        | expr7

expr7 : ( "-" | "!" ) expr7
        | expr8

expr8 : constant
        | lvalue
        | T_THIS
        | call 
        | T_READINTEGER "(" ")"
        | T_READLINE "(" ")"
        | T_NEW T_ID
        | T_NEWARRAY "(" expr "," type ")"
        | "(" expr ")"

lvalue : T_ID
        | expr8 "." T_ID 
        | expr8 "[" expr "]"

call : T_ID "(" actuals ")" 
        | expr8 "." T_ID "(" actuals ")"  

actuals : (expr exprs)?

constant : T_INT_CONSTANT
        | T_DOUBLE_CONSTANT
        | T_BOOL_CONSTANT
        | T_STRING_CONSTANT
        | T_NULL

T_ASSIGN : "="
T_BOOL_CONSTANT : T_FALSE
        | T_TRUE
T_NULL : "null"
T_THIS : "this"
T_VOID : "void"
T_FOR : "for"
T_IF : "if"
T_WHILE : "while"
T_ELSE: "else"
T_CLASS : "class"
T_EXTENDS : "extends"
T_INTERFACE : "interface"
T_IMPLEMENTS : "implemnts"
T_NEW : "new"
T_NEWARRAY : "NewArray"
T_INT : "int"
T_DOUBLE : "double" 
T_BOOL : "bool"
T_STRING : "string"
T_PRIVATE : "private"
T_PROTECTED : "protected"
T_PUBLIC : "public"
T_TRUE : "true"
T_FALSE : "false"
T_AND : "&&"
T_OR : "||"
T_RETURN : "return"
T_BREAK : "break"
T_CONTINUE : "continue"
T_PRINT : "Print"
T_READINTEGER : "ReadInteger"
T_READLINE : "ReadLine"
T_EQUAL : "=="
T_NOT_EQUAL : "!="
T_LESS_THAN_EQUAL : "<="
T_GREATER_THAN_EQUAL : ">="
T_ID : /[a-zA-Z]([a-zA-Z0-9]|\_)*/
T_STRING_CONSTANT : /\d+\.\d*[E,e]\+?\d+/ | /\d+\.\d*/
T_INT_CONSTANT : /0[x|X][\da-fA-F]*/ | /\d+/
T_DOUBLE_CONSTANT : /"[^"^\\n]*"/
SINGLE_LINE_COMMENT : /\/\/[^\\n]*/
MULTI_LINE_COMMENT : /\/\* [.\\n]* \*\//

%import common.WS -> WHITESPACE
%ignore WHITESPACE
%ignore SINGLE_LINE_COMMENT
%ignore MULTI_LINE_COMMENT
"""

parser = Lark(grammar, parser="lalr", debug=True)

error_prog = '''.text
.globl main

main:
la $a0 , errorMsg
addi $v0 , $zero, 4
syscall
jr $ra

.data
errorMsg: .asciiz "Semantic Error"
'''


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
    
    with open(_input, "r") as input_file:
        code = input_file.read()
        lark_tree = parser.parse(code)
        parseTree = build_parser_tree(lark_tree)
        print(parseTree)

    with open(os.path.join("out", _output), "w") as output_file:
        sys.stdout = output_file
        try:
            cgen(parseTree)
        except:
            sys.stdout.close()
            os.remove(os.path.join("out", _output))
            with open(os.path.join("out", _output), "w") as f:
                sys.stdout = f
                emit(error_prog)
        sys.stdout.close()


if __name__ == "__main__":
    main(sys.argv[1:])
