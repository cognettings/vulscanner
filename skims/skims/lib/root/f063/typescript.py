from collections.abc import (
    Iterator,
)
from lib.root.f063.common import (
    get_eval_danger,
    insecure_path_traversal,
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


def ts_insecure_path_traversal(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_PATH_TRAVERSAL

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in insecure_path_traversal(graph, method, method_supplies):
            yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.js_insecure_path_traversal",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def ts_zip_slip_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TS_ZIP_SLIP
    danger_methods = {"createWriteStream"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            if check_methods_expression(
                graph, n_id, danger_methods
            ) and get_eval_danger(graph, n_id, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f063.js_insecure_path_traversal",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
