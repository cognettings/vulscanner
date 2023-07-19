from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.switch_body import (
    build_switch_body_node,
)
from syntax_graph.syntax_nodes.switch_statement import (
    build_switch_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph

    if (body_id := match_ast_d(graph, args.n_id, "switch")) and (
        value_id := graph.nodes[args.n_id].get("label_field_value")
    ):
        return build_switch_statement_node(args, body_id, value_id)

    case_expr = match_ast_group_d(graph, args.n_id, "expression_case")

    if len(case_expr) > 0:
        default_id = match_ast_d(graph, args.n_id, "default_case")
        return build_switch_body_node(args, iter(case_expr), default_id)

    childs = adj_ast(graph, args.n_id)
    return build_switch_statement_node(graph, childs[0], childs[-1])
