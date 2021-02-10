import enum
from CGEN import cgen_global_variable, get_type, get_varieble_data

test_classes = list()
test_interfaces = list()
test_functions = list()
test_variables = list()

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
    classes = list()

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
        if node.data == "VariableDecl":
            cgen_global_variable(child)
    for child in node.children:
        if node.data == "InterfaceDecl":
            init_interface(child)
    for child in node.children:
        if node.data == "ClassDecl":
            init_class(child)
    for child in node.children:
        if node.data == "FunctionDecl":
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
    ret_type = get_type(node)[1]
    name = node.children[1].children[0].data
    in_types = list()
    formals = node.children[3]
    if len(formals.children) >= 1:
        in_types.append(get_type(formals.children[0])[1])
        formals_continue = formals.children[1]
        for fchild in formals_continue.children:
            in_types.append(get_type(fchild)[1])
    return FuncDef(name, None, in_types, ret_type)



def recognize_global_class(node):
    pass


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