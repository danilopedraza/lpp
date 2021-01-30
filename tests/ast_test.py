from unittest import TestCase

from lpp.ast import (
    Identifier,
    LetStatement,
    ExpressionStatement,
    Integer,
    ReturnStatement,
    Expression,
    Program
)

from lpp.token import (
    Token,
    TokenType
)


class ASTTest(TestCase):

    def test_expression_statement(self) -> None:
        # Testing 'x;'
        program: Program = Program(statements=[
            ExpressionStatement(
                token=Token(TokenType.RETURN, literal='x'),
                expression=Identifier(
                    token=Token(TokenType.IDENT, literal='x'),
                    value='x')
            )
        ])

        self.assertEquals(str(program), 'x')

    def test_let_statement(self) -> None:
        # Testing 'variable x = y;'
        program: Program = Program(statements=[
            LetStatement(
                token=Token(TokenType.LET, literal='variable'),
                name=Identifier(
                    token=Token(TokenType.IDENT, literal='x'),
                    value='x'
                ),
                value=Identifier(
                    token=Token(TokenType.IDENT, literal='y'),
                    value='y'
                )
            )
        ])

        self.assertEquals(str(program), 'variable x = y;')
    
    def test_return_statement(self) -> None:
        # Testing 'regresa x;'
        program: Program = Program(statements=[
            ReturnStatement(
                token=Token(TokenType.RETURN, literal='regresa'),
                return_value=Identifier(
                    token=Token(TokenType.IDENT, literal='x'),
                    value='x')
            )
        ])

        self.assertEquals(str(program), 'regresa x;')
