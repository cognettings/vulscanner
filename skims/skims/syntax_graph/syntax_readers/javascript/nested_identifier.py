from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.symbol_lookup import (
    build_symbol_lookup_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_group_d,
)
from utils.graph.text_nodes import (
    n_ids_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    identifiers = match_ast_group_d(graph, args.n_id, "identifier")
    if identifiers:
        var_name = n_ids_to_str(graph, (id for id in identifiers), ".")
    else:
        var_name = ""
    return build_symbol_lookup_node(args, var_name)
