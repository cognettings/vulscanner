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


def _azure_kv_secret_no_expiration_date(graph: Graph, nid: NId) -> NId | None:
    attr, _, _ = get_attribute(graph, nid, "expiration_date")
    if not attr:
        return nid
    return None


def tfm_azure_kv_secret_no_expiration_date(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KV_SECRET_NO_EXPIRATION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_key_vault_secret" and (
                report := _azure_kv_secret_no_expiration_date(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f401.has_not_expiration_date_set",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
