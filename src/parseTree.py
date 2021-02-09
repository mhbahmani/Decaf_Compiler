from lark import Tree

class Node:
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = list()
        self.attr = dict()


    def add_child(self, child):
        self.children.append(child)

    
    def get_type(self):
        return self.attr['type']


    def set_type(self, type):
        self.attr['type'] = type


    def set_arr_lenght(self, length):
        self.attr['arr_length'] = length


    def get_arr_length(self):
        return self.attr['arr_length']



source = None

def build_parser_tree(lark_tree):
    source = Node(lark_tree.data, None)
    for child in lark_tree.children:
        source.add_child(build_node_parse_tree(child, source))
    return source


def build_node_parse_tree(lark_node, parent):
    if isinstance(lark_node, Tree):
        node = Node(lark_node.data, parent)
        for child in lark_node.children:
            node.add_child(build_node_parse_tree(child, node))
    else :
        return Node(lark_node, parent)
    
