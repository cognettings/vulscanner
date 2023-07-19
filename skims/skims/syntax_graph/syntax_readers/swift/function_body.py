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
    ignored_types = {"{", "}"}
    statements = match_ast_d(args.ast_graph, args.n_id, "statements")
    if statements:
        c_ids = adj_ast(args.ast_graph, statements)
    else:
        c_ids = adj_ast(args.ast_graph, args.n_id)
    filtered_ids = [
        _id
        for _id in c_ids
        if args.ast_graph.nodes[_id]["label_type"] not in ignored_types
    ]
    return build_execution_block_node(args, iter(filtered_ids))
