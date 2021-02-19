from mipsCodes import add_data, emit_comment, create_lable, emit_lable, emit_j, emit, emit_li, emit_syscal, emit_sw, emit_sub
from parseTree import Node
from table import scope_handler, PrimitiveType, Variable

def data_label():
    num = 0
    while True:
        yield '__const' + str(num)
        num += 1

data_label_generator = data_label()


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


def cgen_expr(node):
    if len(node.children) == 1:
        if node.children[0].data == 'expr':
            return cgen_expr(node.children[0])
        elif node.children[0].data == 'T_READLINE':
            return cgen_readline(node.children[0]) # TODO define used cgen function, remove this when function added
        elif node.children[0].data == 'T_READINTEGER':
            return cgen_readint(node.children[0])
        elif node.children[0].data == 'call':
            return cgen_call(node.children[0]) # TODO define used cgen function, remove this when function added
        elif node.children[0].data == 'T_THIS':
            raise Exception()
        elif node.children[0].data == 'lvalue':
            return cgen_lvalue(node.children[0]) # TODO define used cgen function, remove this when function added
        elif node.children[0].data == 'constant':
            return cgen_constant(node.children[0])

    elif len(node.children) == 2:
        if node.children[0].data == '!':
            return cgen_expr_not(node)
        elif node.children[0].data == '-':
            return cgen_expr_neg(node)
        elif node.children[0].data == 'T_NEW':
            return cgen_expr_new(node) # TODO define used cgen function, remove this when function added

    elif len(node.children) == 3:
        if node.children[1].data == 'T_ASSIGN':
            return cgen_expr_assign(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == 'T_OR':
            return cgen_expr_or(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == 'T_AND':
            return cgen_expr_and(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == 'T_EQUAL':
            return cgen_expr_equal(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == 'T_NOT_EQUAL':
            return cgen_expr_not_equal(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == 'T_GREATER_THAN_EQUAL':
            return cgen_expr_ge(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == '>':
            return cgen_expr_g(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == 'T_LESS_THAN_EQUAL':
            return cgen_expr_le(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == '<':
            return cgen_expr_l(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == '-':
            return cgen_expr_sub(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == '+':
            return cgen_expr_add(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == '*':
            return cgen_expr_mul(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == '/':
            return cgen_expr_div(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == '%':
            return cgen_expr_mod(node) # TODO define used cgen function, remove this when function added
        elif node.children[1].data == 'expr':
            if node.children[0].data == '(':
                return cgen_expr(node.children[1])
            elif node.children[0].data == 'T_NEWARRAY':
                return cgen_new_array(node) # TODO define used cgen function, remove this when function added


def cgen_expr_not(node): # TODO check
    operand = cgen_expr(node.children[0])
    if operand.type != PrimitiveType.boolean:
        raise Exception()
    emit_lw('$t0', '$fp', operand.address)
    emit_li('$t1', '1')
    emit_sub('$t0', '$t1', '$t0')
    temp = scope_handler.add_temp(PrimitiveType.integer)
    emit_sw('$t0', '$fp', temp.address.offset)
    return temp


def cgen_expr_neg(node): # TODO check
    operand = cgen_expr(node.children[0])
    emit_lw('$t0', '$fp', operand.address)
    emit_sub('$t0', '$zero', '$t0')
    temp = scope_handler.add_temp(PrimitiveType.integer)
    emit_sw('$t0', '$fp', temp.address.offset)
    return temp


def cgen_constant(node): # TODO check !!!IMPORTANT
    if node.children[0].data == 'T_INT_CONSTANT':
        value = node.children[0].data
        if (value[:2].lower() == '0x'):
            value = str(int(value[2:], 16))
        label = next(data_label_generator)
        
        add_data(label, value)
        emit_la('$t0', label)
        emit_lw('$t1', '$t0')
        temp = scope_handler.add_temp(PrimitiveType.integer)
        emit_sw('$t1', '$fp', temp.address.offset)

        return temp

    elif node.children[0].data == 'T_DOUBLE_CONSTANT':
        value = node.children[0].data
        label = next(data_label_generator)
        
        add_data(label, value)
        emit_la('$t0', label)
        emit_lw('$t1', '$t0')
        temp = scope_handler.add_temp(PrimitiveType.double)
        emit_sw('$t1', '$fp', temp.address.offset)

        return temp

    elif node.children[0].data == 'T_BOOL_CONSTANT':
        value = node.children[0].data
        if (value == 'true'):
            value = '1'
        else:
            value = '0'
        label = next(data_label_generator)
        
        add_data(label, value)
        emit_la('$t0', label)
        emit_lw('$t1', '$t0')
        temp = scope_handler.add_temp(PrimitiveType.boolean)
        emit_sw('$t1', '$fp', temp.address.offset)

        return temp

    elif node.children[0].data == 'T_STRING_CONSTANT':
        value = node.children[0].data
        value = '"' + value + '"'
        label = next(data_label_generator)
        
        add_data(label, value)
        emit_la('$t0', label)
        emit_lw('$t1', '$t0')
        temp = scope_handler.add_temp(PrimitiveType.string)
        emit_sw('$t1', '$fp', temp.address.offset)

        return temp

    elif node.children[0].data == 'T_NULL':
        pass # TODO


def cgen_readint(node): # TODO check
    emit_li('$v0', '5')
    emit_syscal()
    integer = scope_handler.add_temp(PrimitiveType.integer)
    # load integer into data section
    emit_sw('$v0', '$fp', integer.address.offset)
    return integer


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
        cgen_while(child)
    elif child.data == "forstmt":
        cgen_for(child)
    elif child.data == "breakstmt":
        cgen_break(child)
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
        scope_handler.add_scope(False)
    
    for child in node.children:
        if child.data == "variabledecl":
            cgen_variable_delc(child.children[0])
        elif child.data == "stmt":
            cgen_stmt(child)
    scope_handler.del_scope()


def cgen_variable_delc(node):
    name, type_var = get_varieble_data(node)
    scope_handler.add_local(type_var, name)

