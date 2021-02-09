import enum


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


def init_decls(node):
    for child in node.children:
        if node.data == "VariableDecl":
            intit_variable(child)
        elif node.data == "FunctionDecl":
            init_function(child)
        elif node.data == "ClassDecl":
            init_class(child)
        elif node.data == "InterfaceDecl":
            init_interface(child)