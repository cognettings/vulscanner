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


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    child_ids = adj_ast(graph, args.n_id)
    left_id = None
    operator_id = ""
    right_id = None
    if len(child_ids) > 2:
        left_id = child_ids[0]
        operator_id = child_ids[1]
        right_id = child_ids[2]
        operator = graph.nodes[operator_id]["label_text"]
    return build_binary_operation_node(args, operator, left_id, right_id)
