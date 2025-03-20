import time
class Executor:
    def __init__(self):
        self.code = None
        self.env = [{}]

    def expect_token(self, token, got):
        if got in token:
            print("'{}' expected; got '{}'".format(token, got[0]))
            exit()

    def interpret_conditional(self, conditonal):
        match conditonal[0]:
            case "TRUE":
                return True
            case "FALSE":
                return False
            case "GREATER":
                return self.interpret_literal(conditonal[1]) > self.interpret_literal(conditonal[2])
            case "LESSER":
                return self.interpret_literal(conditonal[1]) < self.interpret_literal(conditonal[2])
            case "EQUAL":
                return self.interpret_literal(conditonal[1]) == self.interpret_literal(conditonal[2])
            case "NOT_GREATER":
                return not self.interpret_literal(conditonal[1]) > self.interpret_literal(conditonal[2])
            case "NOT_LESSER":
                return not self.interpret_literal(conditonal[1]) < self.interpret_literal(conditonal[2])
            case "NOT_EQUAL":
                return not self.interpret_literal(conditonal[1]) == self.interpret_literal(conditonal[2])

    def interpret_literal(self, literal):
        match literal[0]:
            case "STRING":
                return str(literal[1])
            case "NUMBER":
                return int(literal[1])
            case "VAR_READ":
                return self.env[-1][literal[1]]
            case "PLUS":
                return self.interpret_literal(literal[1]) + self.interpret_literal(literal[2])
            case "MINUS":
                return self.interpret_literal(literal[1]) - self.interpret_literal(literal[2])
            case "MULTIPLY":
                return self.interpret_literal(literal[1]) * self.interpret_literal(literal[2])
            case "DIVIDE":
                return self.interpret_literal(literal[1]) / self.interpret_literal(literal[2])
            case "MODULO":
                return self.interpret_literal(literal[1]) % self.interpret_literal(literal[2])
            case "EXPONENT":
                return self.interpret_literal(literal[1]) ** self.interpret_literal(literal[2])

    def interpret_line(self, line):
        command = line[0]
        match command:
            case "INPUT":
                self.expect_token(["VAR"], line[1])
                self.env[-1][line[1][1]] = input()
            case "CONV_INT":
                self.expect_token(["VAR"], line[1])
                self.env[-1][line[1][1]] = int(self.env[-1][line[1][1]])
            case "CONV_STRING":
                self.expect_token(["VAR"], line[1])
                self.env[-1][line[1][1]] = str(self.env[-1][line[1][1]])
            case "CONV_FLOAT":
                self.expect_token(["VAR"], line[1])
                self.env[-1][line[1][1]] = float(self.env[-1][line[1][1]])
            case "INCREMENT":
                self.expect_token(["VAR"], line[1])
                self.env[-1][line[1][1]] += 1
            case "DECREMENT":
                self.expect_token(["VAR"], line[1])
                self.env[-1][line[1][1]] -= 1
            case "ASSIGN":
                self.expect_token(["VAR"], line[1])
                self.env[-1][line[1][1]] = self.interpret_literal(line[2])
            case "IF":
                if len(line) == 4:
                    self.runblock(line[2]) if self.interpret_conditional(line[1]) else self.runblock(line[3])
                else:
                    self.runblock(line[2]) if self.interpret_conditional(line[1]) else None
            case "WHILE":
                while self.interpret_conditional(line[1]):
                    self.runblock(line[2])
            case "PRINT":
                print(self.interpret_literal(line[1]))
            case "END":
                exit()
            case "FOR":
                for i in range(self.interpret_literal(line[1])):
                    self.runblock(line[2])
            case "SKIP":
                pass #lol

    def runblock(self, code):
        for line in code:
            self.interpret_line(line)
            
    def execute(self, code):
        self.runblock(code)

executor = Executor()