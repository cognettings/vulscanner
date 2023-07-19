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
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    child_ids = adj_ast(graph, args.n_id)
    value_id = child_ids[0]
    if value_id:
        case_value = node_to_str(graph, value_id)
    else:
        case_value = "Default"
    body_id = child_ids[2]
    return build_switch_section_node(args, case_value, [body_id])
