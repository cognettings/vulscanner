from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.pair import (
    build_pair_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    key_id = graph.nodes[args.n_id]["label_field_key"]
    value_id = graph.nodes[args.n_id]["label_field_value"]
    if graph.nodes[key_id]["label_type"] == "computed_property_name" and (
        c_id := match_ast(graph, key_id, "[", "]").get("__0__")
    ):
        key_id = c_id

    return build_pair_node(args, key_id, value_id)
