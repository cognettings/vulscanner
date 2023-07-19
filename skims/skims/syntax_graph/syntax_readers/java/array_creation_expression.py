from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.array import (
    build_array_node,
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
    arr_value = (
        graph.nodes[args.n_id].get("label_field_value")
        or adj_ast(graph, args.n_id)[-1]
    )

    if (
        (dim_expr := match_ast_d(graph, args.n_id, "dimensions_expr"))
        and (childs := match_ast(graph, dim_expr, "[", "]"))
        and childs.get("__0__")
    ):
        arr_value = childs["__0__"]

    return build_array_node(args, (arr_value,))
