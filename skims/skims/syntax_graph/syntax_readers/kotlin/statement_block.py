from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.execution_block import (
    build_execution_block_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids: tuple[NId, ...] = ()
    if block_id := match_ast_d(graph, args.n_id, "statements"):
        c_ids = adj_ast(graph, block_id)
    elif expr := match_ast_d(graph, args.n_id, "call_expression") or (
        expr := match_ast_d(graph, args.n_id, "comparison_expression")
    ):
        c_ids = (expr,)
    else:
        childs = adj_ast(graph, args.n_id)
        if len(childs) > 2:
            c_ids = childs[1:-1]  # ignore { }
    return build_execution_block_node(args, iter(c_ids))
