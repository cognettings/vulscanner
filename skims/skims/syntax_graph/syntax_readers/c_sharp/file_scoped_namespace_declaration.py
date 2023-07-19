from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.file import (
    build_file_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph import (
    adj_ast,
)


def reader(args: SyntaxGraphArgs) -> NId:
    graph = args.ast_graph
    valid_types = {
        "class_declaration",
        "delegate_declaration",
        "enum_declaration",
        "extern_alias_directive",
        "identifier",
        "interface_declaration",
        "record_declaration",
        "record_struct_declaration",
        "struct_declaration",
        "using_directive",
    }
    childs_id = adj_ast(args.ast_graph, args.n_id)

    return build_file_node(
        args,
        c_ids=(
            c_id
            for c_id in childs_id
            if graph.nodes[c_id]["label_type"] in valid_types
        ),
    )
