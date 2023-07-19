from model.graph import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)


def insecure_cookies(graph: Graph, n_id: NId) -> bool:
    if (
        (expr := graph.nodes[n_id].get("expression"))
        and expr.lower().endswith("cookieservice.set")
        and (args_id := g.match_ast_d(graph, n_id, "ArgumentList"))
        and (args_nids := g.adj_ast(graph, args_id[0]))
        and len(args_nids) > 1
    ):
        return True
    return False
