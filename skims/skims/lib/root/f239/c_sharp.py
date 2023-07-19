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


def c_sharp_info_leak_errors(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INFO_LEAK_ERRORS
    danger_set = {"WebHostDefaults.DetailedErrorsKey", '"true"'}
    danger_methods = {"UseSetting"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if check_methods_expression(
                graph, node, danger_methods
            ) and get_node_evaluation_results(
                method,
                graph,
                node,
                danger_set,
                graph_db=method_supplies.graph_db,
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f239.csharp_info_leak_errors",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
