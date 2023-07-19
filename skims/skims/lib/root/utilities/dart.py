from model.graph import (
    Graph,
)
from utils import (
    graph as g,
)


def library_is_imported(graph: Graph, lib_name: str) -> bool:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "Import")
            and (n_exp := node.get("expression"))
            and (n_exp[1:-1] == lib_name)
        )

    return bool(g.filter_nodes(graph, graph.nodes, predicate_matcher))


def get_imported_alias(graph: Graph, lib_name: str) -> str | None:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "Import")
            and (n_exp := node.get("expression"))
            and (n_exp[1:-1] == lib_name)
        )

    nodes = graph.nodes
    for n_id in g.filter_nodes(graph, nodes, predicate_matcher):
        if alias := nodes[n_id].get("label_alias"):
            return alias
    return None
