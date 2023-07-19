from model.graph import (
    NId,
)
from syntax_graph.syntax_nodes.import_statement import (
    build_import_statement_node,
)
from syntax_graph.types import (
    SyntaxGraphArgs,
)
from utils.graph.text_nodes import (
    node_to_str,
)


def reader(args: SyntaxGraphArgs) -> NId:
    node_attrs: dict[str, str] = {
        "expression": node_to_str(args.ast_graph, args.n_id),
    }
    return build_import_statement_node(args, node_attrs)
