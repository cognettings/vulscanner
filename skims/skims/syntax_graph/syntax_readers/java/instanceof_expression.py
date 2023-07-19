from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.binary_operation import (
    build_binary_operation_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    field_left = as_attrs["label_field_left"]
    field_right = as_attrs["label_field_right"]

    return build_binary_operation_node(
        args,
        "InstanceOf",
        field_left,
        field_right,
    )
