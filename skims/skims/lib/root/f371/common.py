from model.graph import (
    Graph,
    NId,
)
from utils import (
    graph as g,
)


def has_set_inner_html(graph: Graph, nid: NId) -> NId | None:
    ast_childs = g.match_ast(graph, nid, "VariableDeclaration")
    child = ast_childs.get("VariableDeclaration")
    if child and graph.nodes[child]["variable"] == "dangerouslySetInnerHTML":
        return child

    return None
