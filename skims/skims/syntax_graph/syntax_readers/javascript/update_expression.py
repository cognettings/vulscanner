from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.unary_expression import (
    build_unary_expression_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)
    val_id = c_ids[0]
    if len(c_ids) >= 1:
        operator = graph.nodes[c_ids[1]].get("label_text")
    else:
        operator = "Unary"

    return build_unary_expression_node(args, operator, val_id)
