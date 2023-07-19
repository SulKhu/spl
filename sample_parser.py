import enum

@enum.unique
class SulLangToken(str, enum.Enum):
  PLUS = "+"
  MINUS = "-"
  EQUAL = "="
  FALSE = "false"

class SulLangParser:
  def __init__(self):
    pass

  @classmethod
  def parse(cls, input: str) -> SulLangToken:
    if input == "+":
      return SulLangToken.PLUS
    if input.isdigit():
      return input
    if input == "-":
      return SulLangToken.MINUS
    if input == "=":
      return SulLangToken.EQUAL
    if input == "False":
      return SulLangToken.FALSE
    return input

class Lexer:
  def __init__(self):
    pass

  @classmethod
  def lex(cls, input: str):
    tokens = []
    commands  = input.split(";")
    for command in commands:
      params = command.split()
      for param in params:
        tokens.append(SulLangParser.parse(param))
    for token in tokens:
      print(token)

Lexer.lex("5 + 5;x = 9;z = 11;   my_list = False")   
