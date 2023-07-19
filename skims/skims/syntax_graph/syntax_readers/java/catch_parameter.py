from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.parameter import (
    build_parameter_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    cp_node = graph.nodes[args.n_id]
    identifier_id = cp_node["label_field_name"]
    identifier_name = node_to_str(graph, identifier_id)

    if catch_type_id := match_ast_d(graph, args.n_id, "catch_type"):
        variable_type = node_to_str(graph, catch_type_id)

    return build_parameter_node(
        args, identifier_name, variable_type, identifier_id
    )
