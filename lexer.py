
from collections import deque

class Lexer:
    
    # create tokens:
    def __init__(self) -> None:
        self.ints = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.chars = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        self.num_ops = ["+", "-", "*", "/", "%"]
        self.comp_ops = [">", "<", "==", "!=", ">=", "<="]
        self.bool_ops = ["&&", "||", "!"]
        self.true = ["t", "r", "u", "e"]
        self.false = ["f", "a", "l", "s", "e"]
        self.functions = {}
        self.functions["print:"] = ["string"]
        self.function_names = ["print"]
        self.call_stack = deque()
        self.variables = {}
        self.variable_names = []
        
    def lex(self, input: str, parameters: bool = False):
        if parameters:
            
            params = []
            
            curr_param = ""
            for c in input:
                if c == "," or c == ";":
                    params.append(curr_param.replace(" ", ""))
                    curr_param = ""
                
                else:   
                     curr_param += c
            
            if curr_param != "":
                params.append(curr_param.replace(" ", ""))
            
            return params
        
        token_list = []
        curr_num = ""
        curr_bool = ""
        curr_call = ""
        curr_index = 0
        start_index = curr_index
        curr_var = None
        next_is_var = False
                
        if len(input) >= 5 and (input[0:6] == "create"):
            function_name = ""
            curr_index = 6
            for c in input[6:len(input)]:
                if c == ":":
                    break
                
                function_name += c
                curr_index += 1
            
            curr_index += 1
            function_name = function_name.replace(" ", "")
            self.functions[function_name] = self.lex(input[curr_index: input.index("{")], True)
            self.function_names.append(function_name)
            
            curr_index = input.index("{")
            
            get_function = deque([])
            get_function.append("{")
            curr_index += 1
            temp_index = curr_index
            
            while len(get_function) != 0:
                if input[curr_index] == "{":
                    get_function.append("{")
                    
                if input[curr_index] == "}":
                    get_function.pop()
                    
                curr_index += 1
            
            token_list += self.lex(input[temp_index: curr_index - 1])
            input = input[curr_index: len(input)]
            token_list += self.lex(input)
            return token_list
            
            
        if len(input) >= 6 and (input[0: 7] == "repeat:"):
            check = ""
            curr_index = 7
            while input[curr_index] != "{":
                check += input[curr_index]
                curr_index += 1
                
            token_list.append(("loop", self.lex(input[7: curr_index])))
            get_loop = deque([])
            get_loop.append("{")
            curr_index += 1
            temp_index = curr_index
            
            while len(get_loop) != 0:
                if input[curr_index] == "{":
                    get_loop.append("{")
                    
                if input[curr_index] == "}":
                    get_loop.pop()
                    
                curr_index += 1
                
            token_list += self.lex(input[temp_index: curr_index - 1])
            input = input[curr_index: len(input)]
            token_list += self.lex(input)
            return token_list
        
        if len(input) >= 2 and (input[0:2] == "if"):
            token_list.append(("conditional", self.lex(input[2:input.index("{")])))
            get_conditional = deque([])
            get_conditional.append("{")
            curr_index = input.index("{") + 1
            start_index = curr_index
            
            while len(get_conditional) != 0:
                if input[curr_index] == "{":
                    get_conditional.append("{")
                    
                if input[curr_index] == "}":
                    get_conditional.pop()
                    
                curr_index += 1
                
            token_list += self.lex(input[start_index:curr_index - 1])
            input = input[curr_index: len(input)]
            token_list += self.lex(input)
            return token_list
            
            
        for c in input:
            if len(input) == 0:
                break
            
            if c in self.chars:
                curr_call += c
            
            if next_is_var:
                try:
                    input.index(":")
                except:
                    next_is_var = True
                
                else:
                    if input[curr_index:input.index(":") + 1] in self.function_names:
                        function_call = (input[curr_index:input.index(":")], self.lex(input[input.index(":") + 1: input.index(";")], True))
                        self.variables[curr_var] = function_call
                        self.variable_names.append(curr_var)
                        token_list.append(function_call)
                        input = input[input.index(";") + 1: len(input)]
                        token_list += self.lex(input)
                        return token_list
                        
                        
            
            if c == ";":
                if curr_num != "":
                    type = ""
                    try:
                        int(curr_num)
                    except:
                        my_num = float(curr_num)
                        type = "float"
                
                    else:
                        my_num = int(curr_num)
                        type = "int"
                    
                    if next_is_var:
                        self.variables[curr_var] = my_num
                        self.variable_names.append(curr_var)
                        token_list.append((curr_var, my_num))
                        curr_num = ""
                    
                    else:
                        token_list.append((type, my_num))
                        
                if curr_call in self.variable_names:
                    token_list.append((curr_call, self.variables[curr_call]))
                    
                token_list += self.lex(input[curr_index + 1: len(input)])
                return token_list
            
            if c == "=":
                if input[curr_index + 1] == "=":
                    
                    if curr_call in self.variable_names:
                        token_list.append((curr_call, self.variables[curr_call]))
                        curr_call = ""
                    
                    if curr_num != "":
                        type = ""
                        try:
                            int(curr_num)
                        except:
                            my_num = float(curr_num)
                            type = "float"
                
                        else:
                            my_num = int(curr_num)
                            type = "int"
                
                        if next_is_var:
                            self.variables[curr_var] = my_num
                            self.variable_names.append(curr_var)
                            token_list.append((curr_var, my_num))
                            curr_num = ""
                
                        else:
                            token_list.append((type, my_num))
                            curr_num = ""
                        
                    token_list.append(("bool_op", "=="))
                
                elif input[curr_index - 1] not in self.bool_ops and input[curr_index - 1] not in self.comp_ops and input[curr_index - 1] != "=":
                    curr_var = input[0: curr_index]
                    self.variable_names.append(curr_var)
                    var = self.lex(input[curr_index + 1: input.index(";") + 1])
                    self.variables[curr_var] = var
                    token_list.append((curr_var, var))
                    input = input[input.index(";") + 1: len(input)]
                    token_list += self.lex(input)
                    
                    return token_list
                    curr_index = 0
                    curr_bool = ""
                    curr_call = ""
            
            if curr_call in self.function_names:
                token_list.append((curr_call, self.lex(input[curr_index + 2: input.index(";")], True)))
                input = input[input.index(";"): len(input)]
                token_list += self.lex(input)
                self.call_stack.append(curr_call)
                return token_list
            
            if c in self.true:
                if curr_bool == "":
                    start_index = curr_index
                curr_bool += c
                
            elif c in self.false:
                if curr_bool == "":
                    start_index = curr_index
                curr_bool += c
                
            if curr_bool == "true" and ((curr_index - start_index) == 3):
                if next_is_var:
                    self.variables[curr_var] = True
                    self.variable_names.append(curr_var)
                    token_list.append((curr_var, True))
                    
                else:
                    token_list.append(("boolean", True))
                    
                curr_bool = ""
                
            if curr_bool == "false" and ((curr_index - start_index) == 4):
                if next_is_var:
                    self.variables[curr_var] = False
                    self.variable_names.append(curr_var)
                    token_list.append((curr_var, False))
                
                else:
                    token_list.append(("boolean", False))
                
                curr_bool = ""
            
            if c in self.ints or c == ".":
                curr_num += c
                
            elif curr_num != "":
                type = ""
                try:
                    int(curr_num)
                except:
                    my_num = float(curr_num)
                    type = "float"
                
                else:
                    my_num = int(curr_num)
                    type = "int"
                
                if next_is_var:
                    self.variables[curr_var] = my_num
                    self.variable_names.append(curr_var)
                    token_list.append((curr_var, my_num))
                    curr_num = ""
                
                else:
                    token_list.append((type, my_num))
                    curr_num = ""
                
            if c in self.num_ops:
                
                if curr_call in self.variable_names:
                    token_list.append((curr_call, self.variables[curr_call]))
                    curr_call = ""
                
                token_list.append(("num_op", c))
                
                
            if c in self.comp_ops:
                
                if curr_call in self.variable_names:
                    token_list.append((curr_call, self.variables[curr_call]))
                    curr_call = ""
                
                if str(c) + str(input[curr_index + 1]) in self.comp_ops:
                    token_list.append(("comp_op", str(c) + str(input[curr_index + 1])))
                
                else:
                    token_list.append(("comp_op", c))
                    
            if curr_index < len(input) - 1 and c == "!" and input[curr_index + 1] == "=":
                
                if curr_call in self.variable_names:
                    token_list.append((curr_call, self.variables[curr_call]))
                    curr_call = ""
                
                token_list.append(("comp_op", "!="))
                    
            if curr_index < len(input) - 1 and c in self.bool_ops and (str(c) + str(input[curr_index + 1])) not in self.comp_ops:
                
                if curr_call in self.variable_names:
                    token_list.append((curr_call, self.variables[curr_call]))
                    curr_call = ""
                
                token_list.append(("bool_op", c))
            
            if curr_index < len(input) - 1 and (str(c) + str(input[curr_index + 1])) in self.bool_ops:
                    
                if curr_call in self.variable_names:
                    token_list.append((curr_call, self.variables[curr_call]))
                    curr_call = ""                    
                    
                token_list.append(("bool_op", str(c) + str(input[curr_index + 1])))
                
            curr_index += 1
        
        if curr_num != "":
            
            type = ""
            try:
                int(curr_num)
            except:
                my_num = float(curr_num)
                type = "float"
                
            else:
                my_num = int(curr_num)
                type = "int"
            
            if next_is_var:
                token_list.append((curr_var, my_num))
                self.variables[curr_var] = my_num
                self.variable_names.append(curr_var)
                    
            else:
                token_list.append((type, my_num))
        
        if curr_call in self.variable_names:
            token_list.append((curr_call, self.variables[curr_call]))
            curr_call = ""
        
        return token_list                               
    
#my_lexer = Lexer()
#my_tokens = my_lexer.lex("5+7.1; y = 1.7; print: 11; if 8<= 4 {my_var = 7; if 8+8 == 5{my_var = 8} } 5 - 5 + 17/2; create sort: my_list, priority, x { x = 1; 9 < 10;} true == false; no = false; 7 != 9.9; 10.00 > 1.1 <= false; this_variable = true; z = sort: 7, 9.9, False;")


#for token in my_tokens:
#    print(str(token))
    
#print(" ")
#print(my_lexer.functions)
#print(my_lexer.function_names)
#print(my_lexer.variables)
#print("-----------")
#print(" ")