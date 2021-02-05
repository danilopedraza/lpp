from typing import (
    cast,
    List,
    Optional
)

import lpp.ast as ast
from lpp.object import (
    Integer,
    Boolean,
    Null,
    Object
)


TRUE = Boolean(True)
FALSE = Boolean(False)
NULL = Null()


def _evaluate_statements(statements: List[ast.Statement]) -> Optional[Object]:
    result: Optional[Object]  = None
    for statement in statements:
        result = evaluate(statement)
    
    return result


def evaluate(node: ast.ASTNode) -> Optional[Object]:
    node_type = type(node)

    if node_type == ast.Program:
        node = cast(ast.Program, node)
        return _evaluate_statements(node.statements)
    
    elif node_type == ast.ExpressionStatement:
        node = cast(ast.ExpressionStatement, node)

        assert node.expression is not None
        return evaluate(node.expression)
    
    elif node_type == ast.Integer:
        node = cast(ast.Integer, node)

        assert node.value is not None
        return Integer(node.value)
    
    elif node_type == ast.Boolean:
        node = cast(ast.Boolean, node)

        assert node.value is not None
        return TRUE if node.value else FALSE
    
    return None
