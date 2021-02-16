from table import init_decls, ecognize_class_functions
from mipsCodes import emit_comment, create_label, emit_label

def cgen(node):
    emit(".text")
    emit_label("main")
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
    else_lable = create_label()
    t1 = cgen_expr(node.children[2])
    #emit_load() load parameter for jump
    cgen_stmt(node.children[4])
    emit_label(else_lable)
    if node.children[5].children[0].data == "T_ELSE":
        end_if_lable = create_label()
        cgen_stmt(node.children[5].children[1])
        emit_label(end_if_lable)
    #not complete
