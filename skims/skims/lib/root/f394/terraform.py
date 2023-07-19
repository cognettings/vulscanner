from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_attribute,
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


def _trail_log_files_not_validated(graph: Graph, nid: NId) -> NId | None:
    attr, attr_val, attr_id = get_attribute(
        graph, nid, "enable_log_file_validation"
    )
    if not attr:
        return nid
    if attr_val.lower() in {"false", "0"}:
        return attr_id
    return None


def tfm_trail_log_files_not_validated(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_CTRAIL_LOG_NOT_VALIDATED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_cloudtrail":
                if report := _trail_log_files_not_validated(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f394.tfm_log_files_not_validated",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
