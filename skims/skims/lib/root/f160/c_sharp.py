from collections.abc import (
    Iterator,
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
from utils.string import (
    complete_attrs_on_set,
)


def c_sharp_file_create_temp_file(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_CREATE_TEMP_FILE
    danger_methods = complete_attrs_on_set({"System.IO.Path.GetTempFileName"})

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("expression") in danger_methods:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f160.c_sharp_file_create_temp_file",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
