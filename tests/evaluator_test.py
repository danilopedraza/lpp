from typing import (
    cast,
    List,
    Tuple
)
from unittest import TestCase

from lpp.ast import Program
from lpp.evaluator import evaluate
from lpp.lexer import Lexer
from lpp.object import (
    Integer,
    Boolean,
    Object
)
from lpp.parser import Parser


class EvaluatorTest(TestCase):

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('verdadero', True),
            ('falso', False)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('1', 1)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)
    
    def _evaluate_tests(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        evaluated = evaluate(program)

        assert evaluated is not None
        return evaluated
    
    def _test_boolean_object(self, evaluated: Object, expected: bool) -> None:
        self.assertIsInstance(evaluated, Boolean)

        evaluated = cast(Boolean, evaluated)
        self.assertEquals(evaluated.value, expected)
    
    def _test_integer_object(self, evaluated: Object, expected: int) -> None:
        self.assertIsInstance(evaluated, Integer)

        evaluated = cast(Integer, evaluated)
        self.assertEquals(evaluated.value, expected)