from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.literal import (
    build_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    value = match_ast_d(graph, args.n_id, "true")
    if not value:
        value = match_ast_d(graph, args.n_id, "false")
    value_text = graph.nodes[value]["label_text"]
    return build_literal_node(args, value_text, "bool")
