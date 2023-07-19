from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_await_expression_node(
    args: SyntaxGraphArgs,
    expression: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        expression_id=expression,
        label_type="AwaitExpression",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(expression)),
        label_ast="AST",
    )

    return args.n_id
