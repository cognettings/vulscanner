from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
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
from utils.graph import (
    adj_ast,
)


def _elb2_has_not_deletion_protection(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    load_balancer, _, load_id = get_attribute(
        graph, val_id, "LoadBalancerAttributes"
    )
    if not load_balancer:
        yield prop_id
    else:
        key_exist = False
        load_attrs = graph.nodes[load_id]["value_id"]
        for c_id in adj_ast(graph, load_attrs):
            key, key_val, _ = get_attribute(graph, c_id, "Key")
            if key and key_val == "deletion_protection.enabled":
                key_exist = True
                _, value, value_id = get_attribute(graph, c_id, "Value")
                if value in FALSE_OPTIONS:
                    yield value_id
        if not key_exist:
            yield load_id


def cfn_elb2_has_not_deletion_protection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ELB2_NOT_DELETION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::ElasticLoadBalancingV2::LoadBalancer":
                for report in _elb2_has_not_deletion_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("src.lib_path.f258.elb2_has_not_deletion_protection"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
