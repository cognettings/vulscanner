from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
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


def _azure_linux_vm_insecure_authentication(
    graph: Graph, nid: NId
) -> NId | None:
    if get_argument(graph, nid, "admin_ssh_key") is None:
        return nid
    return None


def _azure_virtual_machine_insecure_authentication(
    graph: Graph, nid: NId
) -> NId | None:
    if argument := get_argument(graph, nid, "os_profile_linux_config"):
        attr_key, _, _ = get_attribute(graph, argument, "ssh_keys")
        if not attr_key:
            return argument
    return None


def tfm_azure_virtual_machine_insecure_authentication(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_VM_INSEC_AUTH

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                (name := graph.nodes[node].get("name"))
                and name == "azurerm_virtual_machine"
                and (
                    report := _azure_virtual_machine_insecure_authentication(
                        graph, node
                    )
                )
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f015.tfm_azure_virtual_machine_insecure_authentication"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_linux_vm_insecure_authentication(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_LNX_VM_INSEC_AUTH

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                (name := graph.nodes[node].get("name"))
                and name == "azurerm_linux_virtual_machine"
                and (
                    report := _azure_linux_vm_insecure_authentication(
                        graph, node
                    )
                )
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f015.tfm_azure_linux_vm_insecure_authentication"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
