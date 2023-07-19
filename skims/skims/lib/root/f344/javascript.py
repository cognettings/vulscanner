from collections.abc import (
    Iterator,
)
from lib.root.f344.common import (
    local_storage_from_assignment,
    local_storage_from_http,
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


def js_local_storage_with_sensitive_data(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method: MethodsEnum = MethodsEnum.JS_LOCAL_STORAGE_WITH_SENSITIVE_DATA

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if val_id := local_storage_from_http(graph, n_id, method):
                yield shard, val_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f344.local_storage_with_sensitive_data",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JS_LOCAL_STORAGE_WITH_SENSITIVE_DATA,
    )


def js_local_storage_sens_data(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_LOCAL_STORAGE_SENS_DATA_ASSIGNMENT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            for val_id in local_storage_from_assignment(graph, n_id, method):
                yield shard, val_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f344.local_storage_with_sensitive_data",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
