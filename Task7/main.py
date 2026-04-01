from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from ast import *

def print_tokens(tokens):
    print("\nTOKENS")
    for t in tokens:
        print(f"{t.type}:{t.value}", end=" | ")
    print()

def print_ast(tree, indent=0):
    for node in tree:
        print_node(node, indent)

def print_node(node, indent):
    space = "  " * indent

    if isinstance(node, Let):
        print(f"{space}Let({node.name})")
        print_node(node.val, indent + 1)

    elif isinstance(node, Assign):
        print(f"{space}Assign({node.name})")
        print_node(node.val, indent + 1)

    elif isinstance(node, Print):
        print(f"{space}Print")
        print_node(node.expr, indent + 1)

    elif isinstance(node, Num):
        print(f"{space}Num({node.value})")

    elif isinstance(node, Var):
        print(f"{space}Var({node.name})")

    elif isinstance(node, BinOp):
        print(f"{space}BinOp({node.operator.type})")
        print_node(node.left, indent + 1)
        print_node(node.right, indent + 1)

    elif isinstance(node, While):
        print(f"{space}While")
        print_node(node.condition, indent + 1)
        for stmt in node.body:
            print_node(stmt, indent + 1)

    elif isinstance(node, If):
        print(f"{space}If")
        print_node(node.condition, indent + 1)
        for stmt in node.body:
            print_node(stmt, indent + 1)

    else:
        print(f"{space}Unknown: {type(node).__name__}")


with open("code.txt") as f:
    code = f.read()

print("SOURCE CODE")
print(code)

lexer = Lexer(code)
tokens = lexer.tokenize()
print_tokens(tokens)

parser = Parser(tokens)
tree = parser.parse()

print("\nAST")
print_ast(tree)

print("\nOUTPUT")
Interpreter().run(tree)