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
    Boolean,
    Environment,
    Error,
    Function,
    Integer,
    Object
)
from lpp.parser import Parser


class EvaluatorTest(TestCase):

    def test_assignment_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('variable x = 5; x;', 5),
            ('variable x = 2 * 3; x;', 6),
            ('variable x = 2 * 3; variable y = x + 1; y;', 7),
            ('variable x = verdadero; variable y = !x; y;', False)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            if type(expected) == int:
                self._test_integer_object(evaluated, expected)
            elif type(expected) == bool:
                self._test_boolean_object(evaluated, expected)

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
    
    def test_error_handling(self) -> None:
        tests: List[Tuple[str, str]] = [
            ('5 + verdadero;',
             'Discrepancia de tipos: INTEGER + BOOLEAN'),
             
            ('5 + verdadero; 9;',
             'Discrepancia de tipos: INTEGER + BOOLEAN'),
            ('-verdadero;',
             'Operador desconocido: -BOOLEAN'),
            ('verdadero + falso;',
             'Operador desconocido: BOOLEAN + BOOLEAN'),
            ('5; verdadero - falso; 2 + 2;',
             'Operador desconocido: BOOLEAN - BOOLEAN'),
            ('''
                si (2 < 3) {
                    regresa verdadero * falso;
                }
            ''',
            'Operador desconocido: BOOLEAN * BOOLEAN'),
            ('x = 4;', 'Identificador no encontrado: x')
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self.assertIsInstance(evaluated, Error)

            evaluated = cast(Error, evaluated)
            self.assertEquals(evaluated.message, expected)
    
    def test_function_calls(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('variable a = procedimiento(x) {x}; a(5);', 5),
            ('''
                variable a = procedimiento(x) {
                    regresa x;
                };
                a(5);
            ''', 5),
            ('''
                variable a = procedimiento(x) {
                    regresa 2 * x;
                };
                a(5);
            ''', 10),
            ('''
                variable a = procedimiento(x, y) {
                    regresa x + y;
                };
                a(5, 2);
            ''', 7),
            ('''
                variable a = procedimiento(x, y) {
                    regresa x + y;
                };
                a(5, a(2, 1));
            ''', 8),
            ('procedimiento(x){x}(5)', 5)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)

    def test_function_evaluation(self) -> None:
        source: str = 'procedimiento(x) {x + 2;}'
        evaluated = self._evaluate_tests(source)

        self.assertIsInstance(evaluated, Function)

        evaluated = cast(Function, evaluated)
        self.assertEquals(len(evaluated.parameters), 1)
        self.assertEquals(str(evaluated.parameters[0]), 'x')
        self.assertEquals(str(evaluated.body), '(x + 2)')
    
    def test_if_else_evaluation(self) -> None:
        tests: List[Tuple[str, Any]] = [
            ('si (verdadero) {10;}', 10),
            ('si (falso) {10;}', None),
            ('si (falso) {10;} sino {si (verdadero) {1;}}', 1),
            ('si (2 < 1) {1;} sino {falso;}', False),
            #('si (!0) {1;}', 1)
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
    
    def test_return_evaluation(self) -> None:
        tests: List[Tuple[str, int]] = [
            ('regresa 10;', 10),
            ('regresa 1; 2;', 1),
            ('3; regresa 4 / 2;', 2),
            ('''
                si (2 > 1) {
                    si (5 > 3) {
                        regresa 1;
                    }
                    
                    regresa 2;
                }
            ''', 1)
        ]

        for source, expected in tests:
            evaluated = self._evaluate_tests(source)
            self._test_integer_object(evaluated, expected)


    
    def _evaluate_tests(self, source: str) -> Object:
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()
        env: Environment = Environment()

        evaluated = evaluate(program, env)

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
