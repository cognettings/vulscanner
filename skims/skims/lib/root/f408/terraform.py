from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
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


def _api_gateway_access_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    block = get_argument(graph, nid, "access_log_settings")
    if not block:
        return nid
    return None


def tfm_api_gateway_access_logging_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_API_GATEWAY_LOGGING_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_api_gateway_stage" and (
                report := _api_gateway_access_logging_disabled(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f408.tfm_has_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
