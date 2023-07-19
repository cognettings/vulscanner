from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.named_argument import (
    build_named_argument_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    as_attrs = args.ast_graph.nodes[args.n_id]
    var_id = as_attrs["label_field_key"]
    var_name = node_to_str(args.ast_graph, var_id)
    val_id = as_attrs["label_field_value"]
    return build_named_argument_node(args, var_name, val_id)
