from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.element_access import (
    build_element_access_node,
)
from syntax_graph.syntax_nodes.expression_statement import (
    build_expression_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
    match_ast,
    match_ast_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    c_ids = adj_ast(graph, args.n_id)
    if (
        len(c_ids) == 2
        and graph.nodes[c_ids[0]]["label_type"] == "identifier"
        and graph.nodes[c_ids[1]]["label_type"]
        == "unconditional_assignable_selector"
        and (idx_selector := match_ast_d(graph, c_ids[1], "index_selector"))
        and (arg_id := match_ast(graph, idx_selector, "[", "]").get("__0__"))
    ):
        return build_element_access_node(args, c_ids[0], arg_id)

    invalid_childs = {";", "(", ")", "type_cast_expression"}

    return build_expression_statement_node(
        args,
        c_ids=(
            _id
            for _id in c_ids
            if graph.nodes[_id]["label_type"] not in invalid_childs
        ),
    )
