from typing import List
from abc import (
    ABC,
    abstractmethod
)

from lpp.token import Token


class ASTNode(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Statement(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal


class Expression(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token
    
    def token_literal(self) -> str:
        return self.token.literal


class Program(ASTNode):
    
    def __init__(self, statements: List[Statement]) -> None:
        self.statements = statements
    
    def token_literal(self) -> str:
        if (len(self.statements) > 0):
            return self.statements[0].token_literal()
        
        return ''
    
    def __str__(self) -> str:
        return ''.join([str(statement) for statement in self.statements])
        