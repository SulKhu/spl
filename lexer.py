from collections import deque
from lang_parser import LangParser

class Lexer:
    def __init__(self):
        self.curr_final_curly_index = None
        self.my_functions = ["log"]

    # lex method to split string into tokens
    @classmethod
    def lex(self, input: str):
        length = len(input)
        tokens = []
        token_group = []

        # find the defined functions, if any
        try:
            function_index = input.index("create")
        except:
            function_index = None

        # if found a function defenition, find tokens for before the function,
        # inside the function, and after the function, adding them to our token list
        # in the respective manner
        if function_index != None:
            tokens += self.lex(input[0:function_index])
            name = Lexer.get_method_name(input[function_index + 6 : length])
            #self.my_functions.append(name)
            tokens.append(
                (
                    name,
                    Lexer.get_params(input[function_index + 6 : length]),
                    self.lex(self.get_curly_braces(input[function_index:length])),
                )
            )
            tokens += self.lex(
                input[function_index + self.curr_curly_brace_index: length]
            )
            return tokens

        # see if index of conditional exists, if so set it to value of if_index
        try:
            if_index = input.index("if")
        except:
            if_index = -1

        # see if index of loop exists, if so set it to value of loop_index
        try:
            loop_index = input.index("repeat")
        except:
            loop_index = -1
            
        next_index = None
        conditional_or_loop = None
        if if_index != -1 and loop_index != -1:
            next_index = min(if_index, loop_index)
            if next_index == if_index:
                conditional_or_loop = "if"

            else:
                conditional_or_loop = "loop"

        elif if_index != -1 and loop_index == -1:
            next_index = if_index
            conditional_or_loop = "if"

        elif if_index == -1 and loop_index != -1:
            next_index = loop_index
            conditional_or_loop = "loop"

        if next_index != None:
            tokens += self.lex(input[0:next_index])

            if conditional_or_loop == "if":
                tokens.append(
                    (
                        "conditional",
                        self.lex(self.get_check(input[next_index + 2 : length])),
                        self.lex(self.get_curly_braces(input[next_index:length])),
                    )
                )
                tokens += self.lex(
                    input[next_index + self.curr_curly_brace_index: length]
                )
                return tokens

            if conditional_or_loop == "loop":
                tokens.append(
                    (
                        "loop",
                        self.lex(self.get_check(input[next_index + 6 : length])),
                        self.lex(self.get_curly_braces(input[next_index:length])),
                    )
                )
                tokens += self.lex(
                    input[next_index + self.curr_curly_brace_index : length]
                )
                return tokens

        # finds all instances of semi-colon and splits code into chunks
        commands = input.split(";")
        for command in commands:
            # splits those chunks into plain tokens that are separated by a space
            params = command.split()

            # parse those tokens into our token list
            for param in params:
                token_group.append(LangParser.parse(param))

            # if the token group is not empty, do not add list to tokens
            if len(token_group) != 0:
                tokens.append(token_group)
            token_group = []

        # return our final token list
        return tokens

    # static method that will get the name of a method after the keyword "create"
    @staticmethod
    def get_method_name(input: str) -> str:
        return input[0 : input.index(":")].strip()

    # static method that will get the parameters of a method
    @staticmethod
    def get_params(input: str) -> list[str]:
        return input[input.index(":") + 1 : input.index("{")].split(",")

    # instance method that will find the code that lies within certain curly braces
    # makes sure that it accounts for any curly braces inside the outer curly braces
    @classmethod
    def get_curly_braces(self, input: str) -> str:
        start_index = input.index("{") + 1
        index = start_index
        get_braces = deque([])
        get_braces.append("{")

        # using a stack, find the curly braces that align with the first ones
        while len(get_braces) != 0:
            if input[index] == "{":
                get_braces.append("{")
            if input[index] == "}":
                get_braces.pop()
            index += 1

        # set current final curly brace index to self.curr_curly_brace_index
        self.curr_curly_brace_index = index

        # return the string with the first and last curly braces
        return input[start_index : index - 1]

    @classmethod
    def get_check(self, input: str) -> str:
        return input[0 : input.index("{")]

