from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_namespace_node(
    args: SyntaxGraphArgs, name: str, block_id: str
) -> str:
    args.syntax_graph.add_node(
        args.n_id,
        name=name,
        block_id=block_id,
        label_type="Namespace",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block_id)),
        label_ast="AST",
    )

    return args.n_id
