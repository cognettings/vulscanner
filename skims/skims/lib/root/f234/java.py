from collections.abc import (
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils import (
    graph as g,
)


def get_vuln_nodes(graph: Graph, selected_nodes: list[str]) -> set[NId]:
    vuln_nodes: set[NId] = set()
    for n_id in selected_nodes:
        childs = g.match_ast(graph, n_id, "Parameter", "ExecutionBlock")
        param = childs.get("Parameter")
        block = childs.get("ExecutionBlock")

        if not (param and block):
            continue
        exc_name = graph.nodes[param].get("variable")

        for m_id in g.filter_nodes(
            graph,
            nodes=g.adj_ast(graph, str(block), depth=-1),
            predicate=g.pred_has_labels(label_type="MethodInvocation"),
        ):
            m_node = graph.nodes[m_id]
            if (
                m_node["expression"] == "printStackTrace"
                and (symbol_id := m_node.get("object_id"))
                and graph.nodes[symbol_id]["symbol"] == exc_name
            ):
                vuln_nodes.add(m_id)

    return vuln_nodes


def java_info_leak_stacktrace(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in get_vuln_nodes(graph, method_supplies.selected_nodes):
            yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f234.java_info_leak_stacktrace",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_LEAK_STACKTRACE,
    )
