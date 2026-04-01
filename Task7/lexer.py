class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0

    def current_char(self):
        return self.source_code[self.position] if self.position < len(self.source_code) else None

    def advance(self):
        self.position += 1

    def read_number(self):
        number_str = ""
        while self.current_char() and self.current_char().isdigit():
            number_str += self.current_char()
            self.advance()
        return Token("NUMBER", int(number_str))

    def read_identifier(self):
        identifier_str = ""
        while self.current_char() and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            identifier_str += self.current_char()
            self.advance()

        keywords = ["let", "print", "while", "if"]
        if identifier_str in keywords:
            return Token(identifier_str.upper(), identifier_str)

        return Token("IDENT", identifier_str)

    def tokenize(self):
        tokens = []

        while self.current_char():
            current = self.current_char()

            if current.isspace():
                self.advance()

            elif current.isdigit():
                tokens.append(self.read_number())

            elif current.isalpha():
                tokens.append(self.read_identifier())

            elif current == '+':
                tokens.append(Token("PLUS", "+"))
                self.advance()

            elif current == '-':
                tokens.append(Token("MINUS", "-"))
                self.advance()

            elif current == '*':
                tokens.append(Token("MUL", "*"))
                self.advance()

            elif current == '/':
                tokens.append(Token("DIV", "/"))
                self.advance()

            elif current == '=':
                tokens.append(Token("ASSIGN", "="))
                self.advance()

            elif current == '(':
                tokens.append(Token("LPAREN", "("))
                self.advance()

            elif current == ')':
                tokens.append(Token("RPAREN", ")"))
                self.advance()

            elif current == '{':
                tokens.append(Token("LBRACE", "{"))
                self.advance()

            elif current == '}':
                tokens.append(Token("RBRACE", "}"))
                self.advance()

            elif current == '<':
                tokens.append(Token("LT", "<"))
                self.advance()

            elif current == '>':
                tokens.append(Token("GT", ">"))
                self.advance()

            else:
                raise Exception(f"Invalid character: {current}")

        return tokens