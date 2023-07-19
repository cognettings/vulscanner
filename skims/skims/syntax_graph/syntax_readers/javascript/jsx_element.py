from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.jsx_element import (
    build_jsx_element_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast_d,
    match_ast_group_d,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    childs_with_attrs = match_ast_group_d(graph, args.n_id, "jsx_attribute")
    jsx_elements_nested = match_ast_group_d(graph, args.n_id, "jsx_element")
    childs = match_ast_group_d(
        graph, args.n_id, "jsx_opening_element"
    ) + match_ast_group_d(graph, args.n_id, "jsx_self_closing_element")
    for _id in childs:
        attribute = match_ast_d(graph, _id, "jsx_attribute")
        identifier = match_ast_d(graph, _id, "identifier")
        nested_identifier = match_ast_d(graph, _id, "nested_identifier")
        if attribute:
            childs_with_attrs.append(_id)
        if identifier:
            childs_with_attrs.append(identifier)
        if nested_identifier:
            childs_with_attrs.append(nested_identifier)

    if jsx_elements_nested:
        for element in jsx_elements_nested:
            childs_with_attrs.append(element)
    return build_jsx_element_node(args, childs_with_attrs)
