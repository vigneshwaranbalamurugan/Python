from ast import *

class Parser:
    def __init__(self,tokens):
        self.t = tokens
        self.i = 0

    def cur(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def eat(self,typ):
        if self.cur() and self.cur().type == typ:
            self.i += 1
        else:
            raise Exception("Unexpected token")

    def factor(self):
        tok = self.cur()

        if tok.type == "NUMBER":
            self.eat("NUMBER")
            return Num(tok.value)

        if tok.type == "IDENT":
            self.eat("IDENT")
            return Var(tok.value)

        if tok.type == "LPAREN":
            self.eat("LPAREN")
            node = self.expr()
            self.eat("RPAREN")
            return node

    def term(self):
        node = self.factor()
        while self.cur() and self.cur().type in ["MUL","DIV"]:
            op = self.cur(); self.eat(op.type)
            node = BinOp(node,op,self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.cur() and self.cur().type in ["PLUS","MINUS"]:
            op = self.cur(); self.eat(op.type)
            node = BinOp(node,op,self.term())
        return node

    def cond(self):
        l = self.expr()
        op = self.cur(); self.eat(op.type)
        r = self.expr()
        return BinOp(l,op,r)

    def stmt(self):
        tok = self.cur()

        if tok.type == "LET":
            self.eat("LET")
            name = self.cur().value
            self.eat("IDENT")
            self.eat("ASSIGN")
            return Let(name,self.expr())

        if tok.type == "IDENT":
            name = tok.value
            self.eat("IDENT")
            self.eat("ASSIGN")
            return Assign(name,self.expr())

        if tok.type == "PRINT":
            self.eat("PRINT")
            self.eat("LPAREN")
            e = self.expr()
            self.eat("RPAREN")
            return Print(e)

        if tok.type == "WHILE":
            self.eat("WHILE")
            self.eat("LPAREN")
            c = self.cond()
            self.eat("RPAREN")
            self.eat("LBRACE")
            body=[]
            while self.cur().type!="RBRACE":
                body.append(self.stmt())
            self.eat("RBRACE")
            return While(c,body)

        if tok.type == "IF":
            self.eat("IF")
            self.eat("LPAREN")
            c = self.cond()
            self.eat("RPAREN")
            self.eat("LBRACE")
            body=[]
            while self.cur().type!="RBRACE":
                body.append(self.stmt())
            self.eat("RBRACE")
            return If(c,body)

    def parse(self):
        res=[]
        while self.cur():
            res.append(self.stmt())
        return res