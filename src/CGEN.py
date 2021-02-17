from mipsCodes import emit_comment, create_lable, emit_lable, emit_j, emit
from parseTree import Node
from table import scope_handler

def cgen(node):
    emit(".text")
    emit_lable("main")
    node = node.children[0]
    recognize_class_functions(node)
    init_decls(node)


def cgen_global_variable(node):
    emit_comment("cgen global variable")
    name, type_var = get_varieble_data(node)



def get_varieble_data(node): 
    type_var = find_type(node)
    name = find_name(node)
    return name, type_var


def find_name(node):
    return node.children[1].children[0].data


def find_type(node):
    temp_type = node.children[0]
    if temp_type.data == "T_VOID":
        return "void"
    if len(temp_type.children) > 1:
        return temp_type.children[0].children[0].data, len(temp_type.children) - 1
    else :
        return temp_type.children[0].children[0].data



def cgen_if(node):
    emit_comment("cgen for if")
    else_lable = create_lable()
    end_if_lable = create_lable()
    node.add_attribute("else", else_lable)
    node.add_attribute("end", end_if_lable)
    t1 = cgen_expr(node.children[2])
    #emit_load() load parameter for jump to else and type check
    cgen_stmt(node.children[4])
    if node.children[5].children[0].data == "T_ELSE":
        emit_j(node.get_attribute("end"))
    emit_lable(node.get_attribute("else"))
    if node.children[5].children[0].data == "T_ELSE":
        cgen_stmt(node.children[5].children[1])
        emit_lable(node.get_attribute("end"))
    #not complete

def cgen_while(node):
    emit_comment("cgen for while")
    start_while_lable = create_lable()
    end_while_lable = create_lable()
    node.add_attribute("end", end_while_lable)
    node.add_attribute("start", start_while_lable)
    emit_lable(node.get_attribute("start"))
    t1 = cgen_expr(node.children[2])
    #for jump to end and type check
    cgen_stmt(node.children[4])
    emit_j(node.get_attribute("start"))
    emit_lable(node.get_attribute("end"))



def cgen_for(node):
    emit_comment("cgen for for")
    start_for_lable = create_lable()
    end_for_lable = create_lable()
    node.add_attribute("start", start_for_lable)
    node.add_attribute("end", end_for_lable)
    cgen_null_expr(node.children[2])
    emit_lable(node.get_attribute("start"))
    t1 = cgen_expr(node.children[4])
    #for jump to end and type check bool
    cgen_stmt(node.children[8])
    cgen_null_expr(node.children[6])
    emit_j(node.get_attribute("start"))
    emit_lable(node.get_attribute("end"))



def cgen_continue(node):
    emit_comment("cgen for continiue")
    while node.data != "forstms" or node.data != "whilestms":
        if node.data == "functiondecl":
            raise Exception()
        node = node.parent
    emit_j(node.get_attribute("start"))


def cgen_break(node):
    emit_comment("cgen for break")
    while node.data != "forstms" or node.data != "whilestms":
        if node.data == "functiondecl":
            raise Exception()
        node = node.parent
    emit_j(node.get_attribute("end"))


def cgen_return(node):
    emit_comment("cgen for break")
    # checking validity of statement
    func = node.ref_parent
    while func is not None and func.data != "functiondecl":
        func = func.ref_parent

    # return isn't in any function!
    if func is None:
        raise Exception(
            "Error in return node " + str(node) + ", return node must be use in a funcion!"
        )

    # return for void functions
    if node.ref_child[0].data == "nothing":
        if func.ref_child[0].data == "void":
            emit_move("$sp", "$fp")
            emit("jr $ra")
            return
        else:
            raise Exception(
                "Error in return statement for function in node" + str(func) + ", function type must be void"
            )

    # return for non void functions
    type = get_type(func.ref_child[0])  # type of parent function
    expr = cgen_expr(node.ref_child[0])  # expr node of return

    expr.attribute[AttName.address].load()
    emit_move("$v0", "$s0")
    emit_move("$sp", "$fp")
    emit("jr $ra")

    return node.ref_child[0].data != "nothing"



def cgen_null_expr(node):
    emit_comment("cgen for null expr")
    node = node.children[0]
    if node.data == "nothing":
        return None
    else :
        return cgen_expr(node)


def cgen_stmt(node):
    emit_comment("cgen for stmt")
    child =  node.children[0]
    if child.data == "nullexpr":
        cgen_null_expr(child)
    elif child.data == "ifstmt":
        cgen_if(child)
    elif child.data == "whilestmt":
        cgen_while(chile)
    elif child.data == "forstmt":
        cgen_for(child)
    elif child.data == "breakstmt":
        cgen_break(chile)
    elif child.data == "continuestmt":
        cgen_continue(child)
    elif child.data == "returnstmt":
        cgen_return(child)
    elif child.data == "printstmt":
        cgen_print(child)
    elif child.data == "stmtblock":
        cgen_stmtblock(child)


def init_decls(node):
    for child in node.children:
        if child.data == "VariableDecl":
            cgen_global_variable(child)
    for child in node.children:
        if child.data == "InterfaceDecl":
            init_interface(child)
    for child in node.children:
        if child.data == "ClassDecl":
            init_class(child)
    for child in node.children:
        if child.data == "FunctionDecl":
            init_function(child)


def recognize_class_functions(node):
    for child in node.children:
        if child.data == "FunctionDecl":
            recognize_golbal_function(child)
        elif child.data == "InterfaceDecl":
            recognize_global_interface(child)
        elif child.data == "ClassDecl":
            recognize_global_class(child)
        elif child.data  == "VariableDecl":
            recognize_global_variable(child)
    set_class_types(node)
    cgen_global_variables()
    if not check_main_function():
        raise Exception()


def cgen_function(node):
    emit_comment("cgen for functondecl")
    node.children[5].add_attribute("in_func", True)
    #to do


def cgen_stmtblock(node):
    emit_comment("cgen for stmtblock")
    if node.get_attribute("in_func"):
        pass
    else :
        scope_handler.add_scope()
    
    for child in node.children:
        if child.data == "variabledecl":
            cgen_variable_delc(child)
        elif child.data == "stmt":
            cgen_stmt(child)
