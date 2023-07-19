import ast
from collections.abc import (
    Callable,
    Iterator,
)
from typing import (
    cast,
    TypeVar,
)

# Constants
_T = TypeVar("_T")


def parse(content: str) -> ast.AST:
    try:
        tree: ast.AST = ast.parse(content)
    except SyntaxError:
        tree = ast.Module()

    return tree


def iterate_nodes(
    content: str,
    filters: tuple[Callable[[_T], bool], ...],
) -> Iterator[_T]:
    for _node in ast.walk(parse(content)):
        node = cast(_T, _node)
        if all(f(node) for f in filters):
            yield node
