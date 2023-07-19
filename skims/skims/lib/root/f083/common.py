from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)
from utils.string import (
    split_on_last_dot,
)


def get_vuln_nodes(graph: Graph, nid: NId, method: MethodsEnum) -> bool:
    f_name = split_on_last_dot(graph.nodes[nid]["expression"])
    if (
        f_name[1] == "parseXmlString"
        and (args := g.match_ast_d(graph, nid, "ArgumentList"))
        and (childs := g.adj_ast(graph, args))
        and len(childs) > 1
        and get_node_evaluation_results(method, graph, childs[1], set())
    ):
        return True
    return False
