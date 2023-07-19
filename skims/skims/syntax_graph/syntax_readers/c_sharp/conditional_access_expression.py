from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.member_access import (
    build_member_access_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    condition_id = graph.nodes[args.n_id]["label_field_condition"]
    binding_id = (
        match_ast_d(graph, args.n_id, "member_binding_expression")
        or match_ast_d(graph, args.n_id, "element_binding_expression")
        or adj_ast(graph, args.n_id)[-1]
    )

    member = node_to_str(graph, condition_id)
    expression = node_to_str(graph, binding_id)

    return build_member_access_node(
        args, member, expression, binding_id, condition_id
    )
