from collections.abc import (
    Iterator,
)
from lib.root.f070.common import (
    PREDEFINED_SSL_POLICY_VALUES,
    SAFE_SSL_POLICY_VALUES,
)
from lib.root.utilities.cloudformation import (
    get_attribute,
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


def _elb2_uses_insecure_security_policy(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    ssl_policy, ssl_val, ssl_id = get_attribute(graph, val_id, "SslPolicy")

    if (
        ssl_policy
        and ssl_val in PREDEFINED_SSL_POLICY_VALUES
        and ssl_val not in SAFE_SSL_POLICY_VALUES
    ):
        yield ssl_id


def cfn_elb2_uses_insecure_security_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB2_INSECURE_SEC_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::ElasticLoadBalancingV2::Listener":
                for report in _elb2_uses_insecure_security_policy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f070.elb2_uses_insecure_security_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
