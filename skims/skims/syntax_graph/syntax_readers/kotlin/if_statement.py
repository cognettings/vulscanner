from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.if_statement import (
    build_if_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    child_ids = adj_ast(graph, args.n_id)
    condition_id = child_ids[2]
    true_id = child_ids[4]
    if graph.nodes[condition_id]["label_type"] == "parenthesized_expression":
        condition_id = str(match_ast(graph, condition_id).get("__1__"))
    false_id = None
    if len(child_ids) == 7:
        false_id = child_ids[6]
    return build_if_node(args, condition_id, true_id, false_id)
