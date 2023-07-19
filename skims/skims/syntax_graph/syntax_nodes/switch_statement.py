from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_switch_statement_node(
    args: SyntaxGraphArgs,
    body_id: NId,
    value_id: NId,
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=body_id,
        value_id=value_id,
        label_type="SwitchStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(body_id)),
        label_ast="AST",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(value_id)),
        label_ast="AST",
    )

    return args.n_id
