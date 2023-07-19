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


def _azure_key_vault_not_recoverable(graph: Graph, nid: NId) -> NId | None:
    soft_key, soft_val, _ = get_attribute(graph, nid, "soft_delete_enabled")
    pur_key, pur_val, _ = get_attribute(graph, nid, "purge_protection_enabled")
    if (
        not soft_key
        or soft_val.lower() == "false"
        or not pur_key
        or pur_val.lower() == "false"
    ):
        return nid
    return None


def tfm_azure_key_vault_not_recoverable(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_KEY_VAULT_NOT_RECOVER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_key_vault" and (
                report := _azure_key_vault_not_recoverable(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f412.azure_key_vault_not_recoverable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
