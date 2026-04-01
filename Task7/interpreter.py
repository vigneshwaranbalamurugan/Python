from ast import *

class Interpreter:
    def __init__(self):
        self.environment = {}

    def visit(self, node):

        if isinstance(node, Num):
            return node.value

        if isinstance(node, Var):
            return self.environment.get(node.name, 0)

        if isinstance(node, BinOp):
            left_value = self.visit(node.left)
            right_value = self.visit(node.right)

            if node.operator.type == "PLUS":
                return left_value + right_value

            if node.operator.type == "MINUS":
                return left_value - right_value

            if node.operator.type == "MUL":
                return left_value * right_value

            if node.operator.type == "DIV":
                return left_value // right_value

            if node.operator.type == "LT":
                return left_value < right_value

            if node.operator.type == "GT":
                return left_value > right_value

        if isinstance(node, Let) or isinstance(node, Assign):
            value = self.visit(node.val)
            self.environment[node.name] = value

        if isinstance(node, Print):
            result = self.visit(node.expr)
            print(result)

        if isinstance(node, While):
            while self.visit(node.condition):
                for statement in node.body:
                    self.visit(statement)

        if isinstance(node, If):
            if self.visit(node.condition):
                for statement in node.body:
                    self.visit(statement)

    def run(self, syntax_tree):
        for statement in syntax_tree:
            self.visit(statement)