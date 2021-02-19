import enum
from CGEN import cgen_global_variable, get_type, get_varieble_data
from parseTree import Node
from mipsCodes  import emit_comment, add_data, push_stack, emit_move, emit_lw, pop_stack

test_classes = list()
test_interfaces = list()
test_functions = list()
test_variables = list()
class_types = list()

class FuncDef:
    def __init__(self, name, lable, inputs_type, return_type):
        self.name = name
        self.lable = lable
        self.inputs_type = inputs_type
        self.return_type = return_type


class PrimitiveType(enum.Enum):
    integer = "int"
    double = "double"
    string = "string"
    boolean = "bool"
    array = "array"
    null = "null"


class InterfaceDef:
    def __init__(self, name):
        self.name = name
        self.protypes = list()
        self.children = list()

    
    def add_prototype(self, protype):
        self.protypes.append(protype)


    def add_child(self, child):
        self.children.append(child)


class ClassDef_type:
    def __init__(self, name, parent, interfaces):
        self.name = name
        self.parent = parent
        self.children = list()
        self.interfaces = interfaces

    
    def add_child(self, child):
        self.children.append(child)

    
    def set_parrent(self, parent):
        self.parent = parent
    

    def set_interfaces(self, interfaces):
        self.interfaces = interfaces


class ClassDef:
    def __init__(self, name):
        self.name = name
        self.variables = list()
        self.variables_access = list()
        self.functions = list()
        self.functions_access = list()


    def add_variable(self, variable, access):
        self.variables.append(variable)
        self.variables_access.append(access)


    def add_function(self, function, access):
        self.functions.append(function)
        self.functions_access.append(access)


    
class AccessType(enum.Enum):
    Private = "private"
    Protected = "protected"
    Public = "public"
    Nothing = "protected"


def recognize_golbal_function(node):
    ret_type = get_type(node)
    name = node.children[1].children[0].data
    in_types = list()
    formals = node.children[3]
    if len(formals.children) >= 1:
        in_types.append(get_type(formals.children[0]))
        formals_continue = formals.children[1]
        for fchild in formals_continue.children:
            in_types.append(get_type(fchild))
    test_functions.append(FuncDef(name, None, in_types, ret_type))

        
def recognize_global_interface(node):     
    name = node.children[1].children[0].data
    interface = InterfaceDef(name)
    for fchild in node.children:
        if fchild.data == "Prototype" :
            interface.add_prototype(load_prototype(fchild))
    test_interfaces.append(interface)


def load_prototype(node):
    ret_type = get_type(node)
    name = node.children[1].children[0].data
    in_types = list()
    formals = node.children[3]
    if len(formals.children) >= 1:
        in_types.append(get_type(formals.children[0]))
        formals_continue = formals.children[1]
        for fchild in formals_continue.children:
            in_types.append(get_type(fchild))
    return FuncDef(name, None, in_types, ret_type)



def recognize_global_class(node):
    name = node.children[1].children[0].data
    new_class = ClassDef(name)
    for fchild in node.children:
        if fchild.data == "Field":
            access_mode = get_access_mode(fchild)
            field = fchild.children[1]
            if field.data == "VariableDecl":
                new_class.add_variable(get_member_varieble(field), access_mode)
            elif field.data == "FunctionDecl":
                new_class.add_function(get_member_function(field), access_mode)


class Variable:
    def __init__(self, name, type, address):
        self.name = name
        self.type = type
        self.address = address


class AddressType(enum.Enum):
    Global = 0
    Local = 1



class Address:
    def __init__(self, offset, type):
        self.offset = offset
        self.type = type


def recognize_global_variable(node):
    node = node.children[0]
    name, type = get_varieble_data(node)
    addr = Address(0, AddressType.Global)
    var = Variable(name, type, addr)
    test_variables.append(var)


def get_access_mode(node):
    mode = node.children[0].children[0].data
    if mode == "T_PRIVATE":
        return AccessType.Private
    elif mode == "T_PROTECTED":
        return AccessType.Protected
    elif mode == "T_PUBLIC":
        return AccessType.Public
    elif mode == "nothing":
        return AccessType.Nothing


def get_member_varieble(node):
    name, type = get_varieble_data(node)
    addr = Address(0, AddressType.Object)
    return Variable(name, type, addr)


def get_member_function(node):
    return load_prototype(node)


def set_class_types(node):
    for fchild in node.children:
        if fchild.data  == "ClassDecl":
            #to do
            pass




def is_class(name):
    for tclass in test_classes:
        if tclass.name == name:
            return True
    return False



def is_interface(name):
    for inter in test_interfaces:
        if inter.name == name:
            return True
    return False



def get_interface(name):
    for inter in test_interfaces:
        if inter.name == name:
            return inter
    return None


def get_class_type(name):
    for tclass in class_types:
        if tclass.name == name:
            return tclass
    return None


def is_class_type(name):
    for tclass in class_types:
        if tclass.name == name:
            return True
    return False


def is_type(type):
    b = type in PrimitiveType and type != "null"
    return b or is_class_type(type)



def cgen_global_variables():
    emit_comment("cgen global variables")
    count = 0
    for i in range(len(test_variables)):
        if find_global_variable(test_variables[i].name, i) != None:
            raise Exception()
        else :
            test_variables[i].address.offset = 4 * count
            count += 1
    add_data("__global", ".space " + str(4 * count))


def find_global_variable(name, index):
    for j in range(len(test_variables)):
        if j == index:
            break
        if test_variables[j].name == name:
            return test_variables[j]
    return None

    
def check_main_function():
    for i in test_functions:
        if i.name == "main":
            if i.return_type == PrimitiveType.integer:
                if len(i.inputs_type) == 0:
                    return True
                return False
            return False
    return False


class ScopeHandler():
    def __init__(self):
        self.scops = list()

    def add_scope(self, is_function):
        if is_function:
            self.scops.append(Scope(None)
        else :
            self.scops.append(Scope(self.scops[len(self.scops) - 1], offset = self.scops[len(self.scops) - 1].offset + len(self.scops[len(self.scops) - 1].locals)))


    def find_variable(self, name):
        x = find_global_variable(name, len(test_variables))
        if len(self.scops) < 1 and x == None:
            raise Exception()
        s = self.scops[len(self.scops) - 1]
        while s != None:
            x = s.find_variable(name)
            if x != None:
                return x
            s = s.parent
        x = find_global_variable(name, len(test_variables))
        if x == None:
            raise Exception()
        else :
            return x

    def add_param(self, type, name):
        self.scops[len(self.scops) - 1].add_param(type, name)


    def store_and_update_fp(self):
        self.scops[len(self.scops) - 1].store_and_update_fp()
        

    def add_local(self, type, name):
        self.scops[len(self.scops) - 1].add_local(type, name)

    def add_temp(self, type):
        return self.scops[len(self.scops) - 1].add_temprory(type)
    
    def del_scope(self):
        s = self.scops.pop()
        if s.parent != None:
            for var in s,locals:
                emit_addi("$sp", "$sp", "4")
        else:
            emit_lw("$fp", "$fp", 0)
            for var in s,locals:
                emit_addi("$sp", "$sp", "4")
            for var in s,params:
                emit_addi("$sp", "$sp", "4")
            emit_addi("$sp", "$sp", "4")
            emit_addi("$sp", "$sp", "4")

    
class Scope:
    def __init__(self, parent, is_global = False, offset = 0):
            self.params = list()
            self.locals = list()
            self.parent = parent
            self.is_global  = is_global
            self.temp_count = 0
            self.offset = offset
    
    def add_param(self, type, name):
        addr = Address(4*(len(self.params) + 1), AddressType.Local)
        var = Variable(name, type, addr)
        self.params.append(var)
        push_stack("$zero")


    def store_and_update_fp(self):
        push_stack("$fp")
        emit_move("$fp", "$sp")
        push_stack("$zero") #for ra
        

    def add_local(self, type, name):
        addr = Address(-4*(len(self.locals) + 2 + offset), AddressType.Local)
        var = Variable(name, type, addr)
        self.locals.append(var)
        push_stack("$zero")


    def find_variable(self, name):
        for var in self.locals:
            if var.name == name:
                return var
        for var in self.params:
            if var.name == name:
                return var
        return None

    def add_temprory(self, type):
        name = "_t" + str(self.temp_count):
        addr = Address(-4*(len(self.locals) + 2 + offset), AddressType.Local)
        self.temp_count += 1
        var = Variable(name, type, addr)
        self.locals.append(var)
        push_stack("$zero")
        return var

scope_handler = ScopeHandler()


def type_equality(type1, type2):
    if len(type1) != len(type2):
        return False
    if len(type1) == 1:
        return type1 == type2
    else :
        return type1[0] == type2[0] and type2[1] == type1[1]



