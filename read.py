from lexer import Lexer

with open('sample_code.txt', 'r') as file:
    code = file.read().replace('\n', '')

print(code)
print("----------")

my_lexer = Lexer()
tokens = my_lexer.lex(code)

for token in tokens:
    print(token)
    
print("")
print(my_lexer.functions)
print(my_lexer.function_names)
print(my_lexer.variables)