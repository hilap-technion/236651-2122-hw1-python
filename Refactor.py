import ast

def get_parent(n: ast.AST, root: ast.AST):
    for n1 in ast.walk(root):
        for c in ast.iter_child_nodes(n1):
            if n == c:
                return n1

def extract(funcDef: ast.FunctionDef,range:tuple,varname:str):
    return True