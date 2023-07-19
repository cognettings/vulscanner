from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.class_decl import (
    build_class_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    n_attrs = graph.nodes[args.n_id]
    name_id = n_attrs["label_field_name"]
    name = node_to_str(graph, name_id)

    block_id = n_attrs["label_field_body"]
    params_id = n_attrs.get("label_field_type_parameters")
    if params_id and not match_ast(graph, params_id, "(", ")").get("__0__"):
        params_id = None

    return build_class_node(args, name, block_id, params_id)
