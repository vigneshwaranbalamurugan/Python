class Num:
    def __init__(self,value): 
        self.value=value

class Var:
    def __init__(self,name): 
        self.name=name

class BinOp:
    def __init__(self,left,operator,right):
        self.left=left; self.operator=operator; self.right=right

class Let:
    def __init__(self,name,value):
        self.name=name; self.val=value

class Assign:
    def __init__(self,name,value):
        self.name=name; self.val=value

class Print:
    def __init__(self,expr): self.expr=expr

class While:
    def __init__(self,condition,body):
        self.condition=condition; self.body=body

class If:
    def __init__(self,condition,body):
        self.condition=condition; self.body=body