import enum
from CGEN import cgen_global_variable, get_type, get_varieble_data
from parseTree import Node

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
    Object = 2


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
