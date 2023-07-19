from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_optional_attribute,
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


def _aws_sec_group_using_tcp(graph: Graph, nid: NId) -> NId | None:
    if (
        (ingress := get_argument(graph, nid, "ingress"))
        and (protocol := get_optional_attribute(graph, ingress, "protocol"))
        and protocol[1] in {"6", "tcp"}
        and (init_port := get_optional_attribute(graph, ingress, "from_port"))
        and init_port[1] == "80"
    ):
        return protocol[2]
    return None


def tfm_secgroup_uses_insecure_protocol(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AWS_SEC_GROUP_USING_TCP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_security_group" and (
                report := _aws_sec_group_using_tcp(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f332.tfm_aws_sec_group_using_tcp",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
