from model.graph import (
    Graph,
    NId,
)
from syntax_graph.syntax_nodes.method_invocation import (
    build_method_invocation_node,
)
from syntax_graph.syntax_nodes.selector import (
    build_selector_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
    pred_ast,
)
from utils.graph.text_nodes import (
    n_ids_to_str,
    node_to_str,
)


def _reader_invocation_expression(
    graph: Graph,
    args: SyntaxGraphArgs,
    arg_part: str | None,
    id_name: str | None,
    pred_id: str | None,
) -> NId | None:
    if arg_part:
        arg_list = match_ast_d(graph, arg_part, "arguments")
    if id_name:
        child_id = match_ast_d(graph, id_name, "identifier")
        if pred_id and child_id:
            selector_name = n_ids_to_str(graph, iter([pred_id, child_id]), ".")
            return build_method_invocation_node(
                args,
                selector_name,
                child_id,
                arg_list if arg_list else None,
                None,
            )
    return None


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    id_name = match_ast_d(
        graph, args.n_id, "unconditional_assignable_selector"
    ) or match_ast_d(graph, args.n_id, "conditional_assignable_selector")
    selector_name = None
    parent = pred_ast(graph, args.n_id)
    if graph.nodes[parent[0]]["label_type"] == "return_statement" and id_name:
        pred_id = match_ast_d(graph, parent[0], "identifier")
        arg_part = match_ast_d(graph, parent[0], "argument_part", 2)
        if built_node := _reader_invocation_expression(
            graph, args, arg_part, id_name, pred_id
        ):
            return built_node

    al_id = None
    if id_name:
        child_id = match_ast_d(graph, id_name, "identifier")
        if child_id:
            selector_name = node_to_str(graph, child_id)

    arg_id = match_ast_d(graph, args.n_id, "argument_part")
    if arg_id and (al_id := match_ast_d(graph, arg_id, "arguments")):
        return args.generic(args.fork_n_id(al_id))
    return build_selector_node(args, selector_name, None)
