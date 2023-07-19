from collections.abc import (
    Iterator,
)
from lib.root.f070.common import (
    PREDEFINED_SSL_POLICY_VALUES,
    SAFE_SSL_POLICY_VALUES,
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


def _elb2_uses_insecure_security_policy(graph: Graph, nid: NId) -> NId | None:
    if attr := get_attribute(graph, nid, "ssl_policy"):
        if (
            attr[0]
            and attr[1] in PREDEFINED_SSL_POLICY_VALUES
            and attr[1] not in SAFE_SSL_POLICY_VALUES
        ):
            return attr[2]
    return None


def tfm_elb2_uses_insecure_security_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ELB2_INSECURE_SEC_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_lb_listener" and (
                report := _elb2_uses_insecure_security_policy(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f070.elb2_uses_insecure_security_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
