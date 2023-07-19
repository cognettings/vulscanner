from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    children = match_ast_group_d(
        args.ast_graph, args.n_id, "initializer_expression"
    )
    return build_array_node(args, iter(children))
