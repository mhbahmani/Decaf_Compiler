from lark import Lark

grammer = """
Start : Decl Program

Nothing :

Program : Decl Program
        | Nothing

Decl : VariableDecl
        | FunctionDecl
        | ClassDecl
        | InterfaceDecl

VariableDecls : Nothing
        | VariableDecls VariableDecl

VariableDecl : Variable ';'

Variable : Type T_ID
        | T_ID T_ID

Type : T_INT
        | T_DOUBLE
        | T_BOOL
        | T_STRING
        | Type '[' ']'
        | T_ID '[' ']'

FunctionDecl : Type T_ID '(' Formals ')' StmtBlock
        | T_VOID T_ID '(' Formals ')' StmtBlock
        | T_ID T_ID '(' Formals ')' StmtBlock

Formals : Nothing
        | Variable FormalsContinue

FormalsContinue : Nothing
        | ',' Variable FormalsContinue

ClassDecl : T_CLASS T_ID Extends Implements  '{' Fields '}'

Extends : Nothing
        | T_EXTENDS T_ID

Implements : Nothing
        | T_IMPLEMENTS T_ID Ids

Ids : Nothing
        | ',' T_ID Ids

Fields : Nothing
        | Field Fields

Field : AccessMode VariableDecl
        | AccessMode FunctionDecl

AccessMode : Nothing
        | T_PRIVATE
        | T_PROTECTED
        | T_PUBLIC

InterfaceDecl : T_INTERFACE T_ID '{' Prototypes '}'

Prototypes : Nothing
        | Prototype Prototypes

Prototype : Type T_ID '(' Formals ')' ';'
        | T_VOID T_ID '(' Formals ')' ';'
        | T_ID T_ID '(' Formals ')' ';'

StmtBlock : '{' VariableDecls Stmts '}'

Stmt : NullExpr ';'
        | IfStmt
        | WhileStmt
        | ForStmt
        | BreakStmt
        | ContinueStmt
        | ReturnStmt
        | PrintStmt
        | StmtBlock

Stmts : Nothing
        | Stmt Stmts


IfStmt : T_IF '(' Expr ')' Stmt IfExtra

IfExtra : %prec NoElse
        | T_ELSE Stmt

WhileStmt : T_WHILE '(' Expr ')' Stmt

ForStmt : T_FOR '(' NullExpr ';' Expr ';' NullExpr ')' Stmt

ReturnStmt : T_RETURN NullExpr ';'

BreakStmt : T_BREAK ';'

ContinueStmt : T_CONTINUE ';'

PrintStmt : T_PRINT '(' Expr Exprs ')' ';'

Expr : LValue %prec our_hero
        | LValue '=' Expr
        | T_ID %prec our_hero
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
        | '-' Expr %prec Neg
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

NullExpr : Nothing
        | Expr

Exprs : Nothing
        | ',' Expr Exprs

LValue : Expr '.' T_ID
        | Expr '[' Expr ']'

Call : T_ID '(' Actuals ')'
        | Expr '.' T_ID '(' Actuals ')'

Actuals : Nothing
        | Expr Exprs

Constant : T_INT_CONSTANT
        | T_DOUBLE_CONSTANT
        | Bool_Constant
        | T_STRING_CONSTANT
        | T_NULL

Bool_Constant : T_TRUE
	    | T_FALSE

%import common.WS -> WHITESPACE
%ignore WHITESPACE
%ignore SINGLE_LINE_COMMENT
%ignore MULTI_LINE_COMMENT

"""

parser = Lark(grammer, parser='lalr', debug=True)


def main():
    return 0


if __name__ == "__main__":
    main()