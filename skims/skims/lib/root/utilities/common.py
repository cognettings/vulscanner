from collections.abc import (
    Iterator,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.utils import (
    filter_ast,
)
from utils import (
    graph as g,
)


def search_method_invocation_naive(
    graph: Graph, methods: set[str]
) -> Iterator[NId]:
    for n_id in filter_ast(graph, "1", {"MethodInvocation"}):
        for method in methods:
            if method in graph.nodes[n_id]["expression"]:
                yield n_id


def library_is_imported(graph: Graph, lib_name: str) -> bool:
    return bool(
        g.matching_nodes(graph, label_type="Import", expression=lib_name)
    )


def check_methods_expression(
    graph: Graph, node: NId, methods: set[str]
) -> bool:
    for method in methods:
        if method in graph.nodes[node]["expression"]:
            return True
    return False
