from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    n_attrs = args.ast_graph.nodes[args.n_id]
    type_id = n_attrs["label_field_type"]
    cast_type = node_to_str(args.ast_graph, type_id)
    val_id = n_attrs["label_field_value"]

    return build_variable_declaration_node(
        args, "CastExpression", cast_type, val_id
    )
