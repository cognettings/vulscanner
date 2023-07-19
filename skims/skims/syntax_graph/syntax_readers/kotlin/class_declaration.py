from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.class_decl import (
    build_class_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    name = "AnonymousClass"
    name_id = match_ast_d(graph, args.n_id, "simple_identifier")
    if name_id:
        name = node_to_str(graph, name_id)

    block_id = match_ast_d(graph, args.n_id, "class_body")
    if not block_id:
        block_id = str(adj_ast(graph, args.n_id)[-1])

    return build_class_node(args, name, block_id, None)
