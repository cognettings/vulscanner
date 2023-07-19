from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.switch_section import (
    build_switch_section_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    statements = match_ast_d(graph, args.n_id, "statements")
    child_ids = adj_ast(graph, str(statements))
    value_id = match_ast_d(graph, args.n_id, "switch_pattern")

    return build_switch_section_node(args, str(value_id), child_ids)
