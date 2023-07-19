from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.assignment import (
    build_assignment_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    var_id = n_attrs["label_field_left"]
    val_id = n_attrs["label_field_right"]
    if op_id := n_attrs.get("label_field_operator"):
        operator = node_to_str(args.ast_graph, op_id)
    else:
        operator = None

    return build_assignment_node(args, var_id, val_id, operator)
