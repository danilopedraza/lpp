import readline
from typing import List

from lpp.ast import Program
from lpp.evaluator import evaluate
from lpp.object import Environment
from lpp.parser import Parser
from lpp.lexer import Lexer
from lpp.token import(
    Token,
    TokenType
)


EOF_TOKEN: Token = Token(TokenType.EOF, '')


def _print_parse_errors(errors: List[str]):
    for error in errors:
        print(error)


def start_repl() -> None:
    scanned: List[str] = []

    while (source := input('>> ')) != 'salir':
        scanned.append(source)
        lexer: Lexer = Lexer(' '.join(scanned))
        parser: Parser = Parser(lexer)
        
        program: Program = parser.parse_program()

        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue
        
        if evaluated := evaluate(program, Environment()):
            print(evaluated.inspect())
