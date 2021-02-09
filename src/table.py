import enum
from CGEN import cgen_global_variable, get_type

test_classes = list()
test_interfaces = list()
test_functions = list()

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

    
    def add_prototype(self, protype):
        self.protypes.append(protype)


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
        self.functions = list()


    def add_variable(self, variable):
        self.variables.append(variable)


    def add_function(self, function):
        self.functions.append(function)


    


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
        if node.data == "FunctionDecl":
            recognize_golbal_function(child)
        elif node.data == "InterfaceDecl":
            recognize_global_interface(child)
        elif node.data == "ClassDecl":
            recognize_global_class(child)


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

