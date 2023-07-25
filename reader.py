from lexer import Lexer

file = open('sample_code.txt', 'r')
code = file.read().replace('\n', '')

file1 = open('sample_code.txt', 'r')
lines = file1.readlines()
count = 1
for line in lines:
    line = line.strip()
    if len(line) == 0:
        count += 1
        continue
    
    if ((line[len(line) - 1] == ';') or (line[len(line) - 1] == '{') or (line[len(line) - 1] == '}')):
        count += 1
        continue
    
    else:
        print("Syntax Error: Line " + str(count))
        exit()
        
my_lexer = Lexer()
tokens = my_lexer.lex(code)

for token in tokens:
    print(token)