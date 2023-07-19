from collections.abc import (
    Iterator,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.context.search.types import (
    SearchArgs,
    SearchResult,
)
from utils.graph import (
    adj_ast,
    adj_cfg,
)

VAR_MAPPINGS = {
    "VariableDeclaration": "variable",
    "MethodDeclaration": "name",
    "Import": "module",
}


def is_symbol_in_import_values(
    graph: Graph, c_id: NId, searched_symbol: str
) -> bool:
    if graph.nodes[c_id].get("imported_alias") == searched_symbol or (
        not graph.nodes[c_id].get("imported_alias")
        and graph.nodes[c_id].get("imported_value") == searched_symbol
    ):
        return True
    return False


def is_symbol_in_import_statement(
    graph: Graph, import_id: NId, searched_symbol: str
) -> bool:
    n_attrs = graph.nodes[import_id]
    if n_attrs.get("import_type") == "multiple_import":
        for c_id in adj_ast(graph, import_id):
            if is_symbol_in_import_values(graph, c_id, searched_symbol):
                return True
    elif is_symbol_in_import_values(graph, import_id, searched_symbol):
        return True
    return False


def search(args: SearchArgs) -> Iterator[SearchResult]:
    for c_id in adj_cfg(args.graph, args.n_id):
        n_attrs = args.graph.nodes[c_id]
        if (
            n_attrs["label_type"] in VAR_MAPPINGS
            and n_attrs.get(VAR_MAPPINGS[n_attrs["label_type"]]) == args.symbol
        ) or (
            n_attrs["label_type"] == "Import"
            and is_symbol_in_import_statement(args.graph, c_id, args.symbol)
        ):
            yield True, c_id
            break
