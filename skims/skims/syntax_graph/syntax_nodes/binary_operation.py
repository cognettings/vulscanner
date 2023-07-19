from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_binary_operation_node(
    args: SyntaxGraphArgs,
    operator: str,
    left_id: NId | None,
    right_id: NId | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        operator=operator,
        label_type="BinaryOperation",
    )

    if left_id:
        args.syntax_graph.nodes[args.n_id]["left_id"] = left_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(left_id)),
            label_ast="AST",
        )

    if right_id:
        args.syntax_graph.nodes[args.n_id]["right_id"] = right_id
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(right_id)),
            label_ast="AST",
        )

    return args.n_id
