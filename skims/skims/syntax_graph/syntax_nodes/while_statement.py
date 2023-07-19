from model.graph import (
    NId,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def build_while_statement_node(
    args: SyntaxGraphArgs, block: NId, conditional: NId | None
) -> NId:
    args.syntax_graph.add_node(
        args.n_id,
        block_id=block,
        label_type="WhileStatement",
    )

    args.syntax_graph.add_edge(
        args.n_id,
        args.generic(args.fork_n_id(block)),
        label_ast="AST",
    )

    if conditional:
        args.syntax_graph.add_edge(
            args.n_id,
            args.generic(args.fork_n_id(conditional)),
            label_ast="AST",
        )

    return args.n_id
