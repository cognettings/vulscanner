from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.argument_list import (
    build_argument_list_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = match_ast_group_d(graph, args.n_id, "value_argument")
    arg_ids = []
    for _id in c_ids:
        val_id = adj_ast(graph, _id)[0]
        if val_id:
            arg_ids.append(val_id)
    return build_argument_list_node(args, iter(arg_ids))
