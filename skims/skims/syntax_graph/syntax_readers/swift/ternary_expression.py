from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.ternary_operation import (
    build_ternary_operation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    cond_id = n_attrs["label_field_condition"]
    false_id = n_attrs["label_field_if_false"]
    true_id = n_attrs["label_field_if_true"]
    return build_ternary_operation_node(args, cond_id, false_id, true_id)
