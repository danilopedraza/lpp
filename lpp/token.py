from enum import (
    auto,
    Enum,
    unique
)

from typing import (
    NamedTuple,
    Dict
)


@unique
class TokenType(Enum):
    ASSIGN = auto()
    COMMA = auto()
    DIVISION = auto()
    ELSE = auto()
    EOF = auto()
    EQ = auto()
    FALSE = auto()
    FUNCTION = auto()
    GT = auto()
    GT_OR_EQ = auto()
    IDENT = auto()
    IF = auto()
    ILLEGAL = auto()
    INT = auto()
    LBRACE = auto()
    LET = auto()
    LPAREN = auto()
    MINUS = auto()
    MULTIPLICATION = auto()
    NOT = auto()
    NOT_EQ = auto()
    PLUS = auto()
    LT = auto()
    LT_OR_EQ = auto()
    RBRACE = auto()
    RETURN = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    TRUE = auto()

class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'falso' : TokenType.FALSE,
        'procedimiento': TokenType.FUNCTION,
        'regresa' : TokenType.RETURN,
        'si' : TokenType.IF,
        'sino' : TokenType.ELSE,
        'variable': TokenType.LET,
        'verdadero' : TokenType.TRUE
    }

    return keywords.get(literal, TokenType.IDENT)
