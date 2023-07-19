from collections.abc import (
    Iterable,
)
from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_jsx_element_node(args: SyntaxGraphArgs, c_ids: Iterable[NId]) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        label_type="JsxElement",
    )
    for c_id in c_ids:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(c_id)),
            label_ast="AST",
        )

    return args.n_id
