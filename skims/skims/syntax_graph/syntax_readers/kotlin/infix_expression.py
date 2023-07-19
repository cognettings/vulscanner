from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.binary_operation import (
    build_binary_operation_node,
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
    if len(c_ids) == 3:
        right_id = c_ids[0]
        operator = node_to_str(graph, c_ids[1])
        left_id = c_ids[2]
    else:
        right_id = None
        operator = "UndefinedInfix"
        left_id = None

    return build_binary_operation_node(
        args,
        operator,
        left_id,
        right_id,
    )
