import enum


@enum.unique
class LangToken(str, enum.Enum):
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    MOD = "%"
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_OR_EQUAL = ">="
    LESS_OR_EQUAL = "<="
    NOT_EQUAL = "!="
    EQUAL_VALUE = "=="
    OR = "||"
    AND = "&&"
    EQUAL = "="
    TRUE = "true"
    FALSE = "false"