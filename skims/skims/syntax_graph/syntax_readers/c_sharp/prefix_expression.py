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
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)

    if len(c_ids) == 2:
        prefix = node_to_str(graph, c_ids[0])
        expression_id = c_ids[1]
    else:
        expression_id = c_ids[0]
        prefix = "Undefined"

    return build_unary_expression_node(args, prefix, expression_id)
