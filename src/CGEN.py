from table import init_decls, ecognize_class_functions
from mipsCodes import emit_comment, create_lable, emit_lable, emit_j, emit
from parseTree import Node

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
        emit_lable(end_if_lable)
    #not complete

def cgen_while(node):
    emit_comment("cgen for while")
    start_while_lable = create_lable()
    end_while_lable = create_lable()
    node.add_attribute("end", end_while_lable)
    node.add_attribute("start", start_while_lable)
    emit_lable(start_while_lable)
    t1 = cgen_expr(node.children[2])
    #for jump to end and type check
    cgen_stmt(node.children[4])
    emit_j(node.get_attribute("start"))
    emit_lable(node.get_attribute("end"))



def cgen_for(node):
    start_for_lable = create_lable()
    end_for_lable = create_lable()
    node.add_attribute("start", start_for_lable)
    node.add_attribute("end", end_for_lable)
    emit_lable(node.get_attribute("start"))
    cgen_null_expr(node.children[2])
    t1 = cgen_expr(node.children[4])
    #for jump to end and type check bool
    cgen_stmt(node.children[8])
    cgen_null_expr(node.children[6])
    emit_j(node.get_attribute("start"))
    emit_lable(node.get_attribute("end"))



def cgen_continue(node):
    while node.data != "forstms" or node.data != "whilestms":
        if node.data == "functiondecl":
            raise error()
        node = node.parent
    emit_j(node.get_attribute("start"))




