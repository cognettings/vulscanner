from model.graph import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)


def json_parse_unval_data(
    graph: Graph,
    n_id: NId,
) -> bool:
    danger_expressions = {
        "localStorage.getItem",
        "sessionStorage.getItem",
    }
    for m_id in g.get_nodes_by_path(
        graph, n_id, [], "ArgumentList", "MethodInvocation"
    ):
        if (exp := graph.nodes[m_id].get("expression")) and (
            exp in danger_expressions
        ):
            return True
    return False
