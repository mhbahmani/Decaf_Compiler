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
    else_lable = create_lable()
    t1 = cgen_expr(node.children[2])
    #emit_load() load parameter for jump
    cgen_stmt(node.children[4])
    emit_lable(else_lable)
    if node.children[5].children[0].data == "T_ELSE":
        end_if_lable = create_lable()
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
    #for jump to end
    cgen_stmt(node.children[4])
    emit_j(node.get_attribute("start"))
    emit_lable(node.get_attribute("end"))


