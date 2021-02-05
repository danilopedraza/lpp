from typing import (
    Any,
    cast,
    List,
    Tuple
)
from unittest import TestCase

from lpp.ast import Program
from lpp.evaluator import (
    evaluate,
    NULL
)
from lpp.lexer import Lexer
from lpp.object import (
    Integer,
    Boolean,
    Object
)
from lpp.parser import Parser


class EvaluatorTest(TestCase):

    def test_bang_operator(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('!verdadero', False),
            ('!falso', True),
            ('!!verdadero', True),
            ('!1', False),
            ('!!1', True),
            #('!0', True)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)

    def test_boolean_evaluation(self) -> None:
        tests: List[Tuple[str, bool]] = [
            ('verdadero', True),
            ('falso', False),
            ('5 > 2', True),
            ('verdadero != falso', True),
            ('(-5 < 2) == falso', False)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_boolean_object(evaluated, expected)
    
    def test_if_else_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('si (verdadero) {10;}', 10),
            ('si (falso) {10;}', None),
            ('si (falso) {10;} sino {si (verdadero) {1;}}', 1),
            ('si (2 < 1) {1;} sino {falso;}', False)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)

            if type(expected) == int:
                self._test_integer_object(evaluated, expected)
            elif type(expected) == bool:
                self._test_boolean_object(evaluated, expected)
            else:
                self._test_null_object(evaluated)

    def test_integer_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('5', 5),
            ('1', 1),
            ('-100', -100),
            ('-52', -52),
            ('2 + 2 + 2', 6),
            ('2 * 2 * 2', 8),
            ('(2 + 7) / 3', 3)
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
    
    def _test_null_object(self, evaluated: Object) -> None:
        self.assertEquals(evaluated, NULL)
