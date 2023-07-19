from collections.abc import (
    Iterable,
)
from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_catch_clause_node(
    args: SyntaxGraphArgs,
    block_node: NId | None,
    children_ids: Iterable[NId] | None,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="CatchClause",
    )

    if block_node:
        args.syntax_graph.nodes[args.n_id]["block_id"] = block_node
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(block_node)),
            label_ast="AST",
        )

    if children_ids:
        for _id in children_ids:
            args.syntax_graph.add_edge(
                args.n_id,
                args.generic(args.fork_n_id(_id)),
                label_ast="AST",
            )

    return args.n_id
