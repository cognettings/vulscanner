from collections.abc import (
    Iterator,
)
from lib.root.utilities.common import (
    check_methods_expression,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from networkx import (
    Graph,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)
from utils.string import (
    build_attr_paths,
)


def check_member_in_paths(graph: Graph, node: NId) -> bool:
    paths = build_attr_paths("System", "Reflection", "Assembly", "Load")
    if (
        (member := g.match_ast_d(graph, node, "MemberAccess"))
        and (expr := graph.nodes[member].get("expression"))
        and (memb := graph.nodes[member].get("member"))
        and (f"{expr}.{memb}" in paths)
    ):
        return True
    return False


def c_sharp_insecure_assembly_load(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_ASSEMBLY_LOAD

    danger_method = {"Load"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                check_methods_expression(graph, node, danger_method)
                and check_member_in_paths(graph, node)
                and get_node_evaluation_results(
                    method,
                    graph,
                    node,
                    set(),
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f413.insecure_assembly_load",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
