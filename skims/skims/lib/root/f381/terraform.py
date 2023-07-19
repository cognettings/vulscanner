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


def _check_required_version(graph: Graph, nid: NId) -> NId | None:
    attr, _, _ = get_attribute(graph, nid, "required_version")
    if not attr:
        return nid
    return None


def tfm_check_required_version(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CHECK_REQUIRED_VERSION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "terraform":
                if report := _check_required_version(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f381.tfm_check_required_version",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
