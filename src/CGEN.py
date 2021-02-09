from table import init_decls, ecognize_class_functions
from mipsCodes import emit_comment

def cgen(node):
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
        return False, "void"
    if temp_type.data == "T_ID":
        return False, temp_type.children[0].data
    else :
        if temp_type.children[0] == "Type" or temp_type.children[0] == "T_ID":
            return True, temp_type
        else :
            return False, temp_type.children[0].children[0].data
