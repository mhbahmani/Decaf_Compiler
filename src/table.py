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


class ClassDef:
     def __init__(self, name):
        self.name = name
        self.variables = list()
        self.functions = list()

