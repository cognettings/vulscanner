from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.variable_declaration import (
    build_variable_declaration_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    match_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    match = match_ast(graph, args.n_id, "declare")
    decl_id = match.get("__0__")
    return build_variable_declaration_node(args, "DeclareVar", None, decl_id)
