from unittest import TestCase
from lpp.ast import (
    LetStatement,
    Program
)
from lpp.lexer import Lexer
from lpp.parser import Parser

class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = 'variable x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)
    
    def test_let_statements(self) -> None:
        source: str = 'variable x = 5;\nvariable y = 10;\nvariable z = 20;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        for i in range(len(program.statements)):
            self.assertEqual(str(program.statements[i])[:10], source.splitlines()[i][:10])
            self.assertIsInstance(program.statements[i], LetStatement)

