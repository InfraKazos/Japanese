from lexer import lexer
from parser import parser
from executor import executor

import sys

code = None

with open(sys.argv[1], "r", encoding = "utf-8") as file:
    code = file.read()

lexer.input(code)
out = parser.parse(code)
executor.execute(out)