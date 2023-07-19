from collections.abc import (
    Iterable,
)
from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_modifiers_node(
    args: SyntaxGraphArgs, modifiers_ids: Iterable[NId]
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="Modifiers",
    )

    for at_id in modifiers_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(at_id)),
            label_ast="AST",
        )

    return args.n_id
