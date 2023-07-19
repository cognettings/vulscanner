from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.member_access import (
    build_member_access_node,
)
from syntax_graph.types import (
    MissingCaseHandling,
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    child_ids = adj_ast(graph, args.n_id)
    if len(child_ids) == 2:
        if graph.nodes[child_ids[1]]["label_type"] == "navigation_suffix" and (
            identifier_id := match_ast(graph, child_ids[1]).get("__1__")
        ):
            member = node_to_str(graph, identifier_id)
        else:
            member = node_to_str(graph, child_ids[1])

        expression = node_to_str(graph, child_ids[0])
        return build_member_access_node(args, member, expression, child_ids[0])
    raise MissingCaseHandling(
        f"Bad Navigation Expression handling in {args.n_id}"
    )
