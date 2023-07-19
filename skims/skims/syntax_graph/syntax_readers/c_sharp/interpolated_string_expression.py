from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.string_literal import (
    build_string_literal_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    value = node_to_str(graph, args.n_id)
    interpolated_ids = match_ast_group_d(graph, args.n_id, "interpolation")
    declaration_ids = (
        var_id
        for _id in interpolated_ids
        for var_id in adj_ast(graph, _id)
        if graph.nodes[var_id]["label_type"] not in {"{", "}", ","}
    )

    return build_string_literal_node(args, value, declaration_ids)
