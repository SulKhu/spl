from lang_token import LangToken

class LangParser:
    def __init__(self):
        self.functions = ["print"]

    # parse method to return the token for the respective string
    @classmethod
    def parse(self, input: str) -> LangToken:
        if input == "+":
            return LangToken.PLUS

        if input == "-":
            return LangToken.MINUS

        if input == "*":
            return LangToken.MULTIPLY

        if input == "/":
            return LangToken.DIVIDE

        if input == "%":
            return LangToken.MOD

        if input == "=":
            return LangToken.EQUAL

        if input == "false":
            return LangToken.FALSE

        if input == "true":
            return LangToken.TRUE

        if input == ">":
            return LangToken.GREATER_THAN

        if input == "<":
            return LangToken.LESS_THAN

        if input == ">=":
            return LangToken.GREATER_OR_EQUAL

        if input == "<=":
            return LangToken.LESS_OR_EQUAL

        if input == "!=":
            return LangToken.NOT_EQUAL

        if input == "==":
            return LangToken.EQUAL_VALUE

        if input == "||":
            return LangToken.OR

        if input == "&&":
            return LangToken.AND

        return input


