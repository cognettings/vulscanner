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


def c_sharp_path_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_PATH_INJECTION
    paths = build_attr_paths("System", "IO", "File", "Open")
    danger_methods = {"Open"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for node in method_supplies.selected_nodes:
            if check_methods_expression(graph, node, danger_methods) and (
                (member := g.match_ast_d(graph, node, "MemberAccess"))
                and (n_attrs := graph.nodes[member])
                and f'{n_attrs["expression"]}.{n_attrs["member"]}' in paths
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
        desc_key="lib_root.f098.c_sharp_path_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
