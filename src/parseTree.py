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
        return aselfttr['type']


    def set_type(self, type):
        self.attr['type'] = type


    def set_arr_lenght(self, length):
        self.attr['arr_length'] = length


    def get_arr_length(self):
        return self.attr['arr_length']



source = None

def build_parser_tree(larktree):
    source = Node(larktree.data, None)
    for child in larktree.children:
        source.add_child(build_node_parse_tree(child, source))
    return source


def build_node_parse_tree(larknode, parent):
    if isinstance(larknode, Tree):
        node = Node(larknode.data, parent)
        for child in larknode.children:
            node.add_child(build_node_parse_tree(child, node))
    else :
        return Node(larknode, parent)
    
