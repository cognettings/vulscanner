from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.reserved_word import (
    build_reserved_word_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    childs = match_ast(args.ast_graph, args.n_id)
    if c_id := childs.get("__1__"):
        expression = f"PackageName {node_to_str(args.ast_graph, c_id)}"
    else:
        expression = "PackageName Unnamed"
    return build_reserved_word_node(args, expression)
