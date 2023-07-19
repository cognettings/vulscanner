from model.graph import (
    Graph,
    MethodSupplies,
    NId,
)


def nid_uses_console_log(
    graph: Graph, method_supplies: MethodSupplies
) -> list[NId]:
    vuln_nodes: list[NId] = []
    for n_id in method_supplies.selected_nodes:
        if graph.nodes[n_id].get("expression") == "console.log":
            vuln_nodes.append(n_id)
    return vuln_nodes
