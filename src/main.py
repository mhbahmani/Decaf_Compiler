from lark import Lark
import sys, getopt

grammer = """
Start : Program

Nothing :

Program : Decl+

Decl : VariableDecl
        | FunctionDecl
        | ClassDecl
        | InterfaceDecl

VariableDecls : VariableDecl+

VariableDecl : Variable ';'

Variable : Type T_ID

Type : T_INT (Array)+
        | T_DOUBLE (Array)+
        | T_BOOL (Array)+
        | T_STRING (Array)+
        | T_ID  (Array)+


Array: '[]'

FunctionDecl : Type T_ID '(' Formals ')' StmtBlock
        | T_VOID T_ID '(' Formals ')' StmtBlock


Formals : (Variable FormalsContinue)?

FormalsContinue : (',' Variable)*

ClassDecl : T_CLASS T_ID Extends Implements  '{' Field* '}'

Extends : T_EXTENDS T_ID
        | nothing

Implements : T_IMPLEMENTS T_ID Ids
        |nothing

Ids : (',' T_ID)*

Fields : Field*

Field : AccessMode VariableDecl
        | AccessMode FunctionDecl

AccessMode : T_PRIVATE
        | T_PROTECTED
        | T_PUBLIC
        | nothing

InterfaceDecl : T_INTERFACE T_ID '{' Prototype* '}'

Prototypes : Prototype*

Prototype : Type T_ID '(' Formals ')' ';'
        | T_VOID T_ID '(' Formals ')' ';'


StmtBlock : '{' VariableDecls Stmt* '}'

Stmt : NullExpr ';'
        | IfStmt
        | WhileStmt
        | ForStmt
        | BreakStmt
        | ContinueStmt
        | ReturnStmt
        | PrintStmt
        | StmtBlock

Stmts : Stms*


IfStmt : T_IF '(' Expr ')' Stmt IfExtra

IfExtra : (T_ELSE Stmt)?

WhileStmt : T_WHILE '(' Expr ')' Stmt

ForStmt : T_FOR '(' NullExpr ';' Expr ';' NullExpr ')' Stmt

ReturnStmt : T_RETURN NullExpr ';'

BreakStmt : T_BREAK ';'

ContinueStmt : T_CONTINUE ';'

PrintStmt : T_PRINT '(' Expr Exprs ')' ';'

Expr : LValue
        | LValue '=' Expr
        | T_ID
        | T_ID '=' Expr
        | Constant
        | T_THIS
        | Call
        | '(' Expr ')'
        | Expr '+' Expr
        | Expr '-' Expr
        | Expr '*' Expr
        | Expr '/' Expr
        | Expr '%' Expr
        | Expr '<' Expr
        | Expr  T_LESS_THAN_EQUAL Expr
        | Expr '>' Expr
        | Expr T_GREATER_THAN_EQUAL Expr
        | Expr T_EQUAL Expr
        | Expr T_NOT_EQUAL Expr
        | Expr T_AND Expr
        | Expr T_OR Expr
        | '-' Expr
        | '!' Expr
        | T_READINTEGER '(' ')'
        | T_READLINE '(' ')'
        | T_NEW T_ID
        | T_NEWARRAY '(' Expr ',' Type ')'
        | T_NEWARRAY '(' Expr ',' T_ID ')'
        | T_ITOD '(' Expr ')'
        | T_DITOI '(' Expr ')'
        | T_ITOB '(' Expr ')'
        | T_BTOI '(' Expr ')'

NullExpr : (Expr)?

Exprs : (',' Expr)*

LValue : Expr '.' T_ID
        | Expr '[' Expr ']'

Call : T_ID '(' Actuals ')'
        | Expr '.' T_ID '(' Actuals ')'

Actuals : (Expr Exprs)?

Constant : T_INT_CONSTANT
        | T_DOUBLE_CONSTANT
        | Bool_Constant
        | T_STRING_CONSTANT
        | T_NULL

Bool_Constant : T_TRUE
	    | T_FALSE

T_VOID: 'void'
T_INT: 'int'
T_DOUBLE: 'double'
T_BOOL: 'bool'
T_STRING: 'string'
T_CLASS: 'class'
T_INTERFACE: 'interface'
T_NULL: 'null'
T_THIS: 'this'
T_EXTENDS: 'extends'
T_IMPLEMENTS: 'implemnts'
T_FOR: 'for'
T_WHILE: 'while'
T_IF: 'if'
T_ELSE: 'else'
T_RETURN: 'return'
T_BREAK: 'break'
T_CONTINUE: 'continue'
T_NEW: 'new'
T_NEWARRAY: 'NewArray'
T_PRINT: 'Print'
T_READINTEGER: 'ReadInteger'
T_READLINE: 'ReadLine'
T_DITOI: 'ditol'
T_ITOD: 'itod'
T_BTOI: 'btoi'
T_ITOB: 'itob'
T_PRIVATE: 'private'
T_PROTECTED: 'protected'
T_PUBLIC: 'public'
T_TRUE: 'true'
T_FALSE: 'false'
T_AND: '&&'
T_OR: '\|\|'
T_EQUAL: '=='
T_NOT_EQUAL: '!='
T_LESS_THAN_EQUAL: '<='
T_GREATER_THAN_EQUAL: '>='
T_ID: /[a-zA-Z]([a-zA-Z0-9]|\_)*/
T_STRING_CONSTANT: /\d+\.\d*[E,e]\+?\d+/ | /\d+\.\d*/
T_INT_COSTANT: /0[x|X][\da-fA-F]*/ | /\d+/
T_DOUBLE_CONSTANT: /"[^"^\n]*"/
WHITE_SPACE: /[ \r\f\s\t\n]/
SINGLE_LINE_COMMENT: /\/\/[^\n]*/
MULTI_LINE_COMMENT: //\* [.\n]* \\\*/
%import common.WS -> WHITESPACE
%ignore WHITE_SPACE
%ignore SINGLE_LINE_COMMENT
%ignore MULTI_LINE_COMMENT

"""

# parser = Lark(grammer, parser='lalr', debug=True)


def main(argv):
    _input = ''
    _output = ''
    if (len(argv) % 2 != 0):
        sys.stderr.write('invalid command, should be like: main.py -i <input file> -o <output file>\n')
        sys.exit(2)
    for i in range(0, len(argv), 2):
        if (argv[i] == '-i' or argv[i] == '--ifile'):
            _input = argv[i + 1]
        elif (argv[i] == '-o' or argv[i] == '--ofile'):
            _output = argv[i + 1]

    if _input == '':
        sys.stderr.write('no input file provided!\n')
        sys.exit(2)
    if _output == '':
        sys.stderr.write('no output file provided!\n')
        sys.exit(2)
    return 0


if __name__ == "__main__":
    main(sys.argv[1:])