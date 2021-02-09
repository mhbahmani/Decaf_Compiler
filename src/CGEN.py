from table import init_decls

def cgen(node):
    node = node.children[0]
    init_decls(node)