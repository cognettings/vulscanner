from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs = adj_ast(args.ast_graph, args.n_id)
    if len(childs) == 5:
        return build_if_node(args, childs[0])
    return args.n_id
