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


def _use_default_security_group(graph: Graph, nid: NId) -> NId | None:
    sec_groups, _, _ = get_attribute(graph, nid, "security_groups")
    vpc_sec_groups, _, _ = get_attribute(graph, nid, "vpc_security_group_ids")
    if not (sec_groups or vpc_sec_groups):
        return nid
    return None


def tfm_ec2_use_default_security_group(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.EC2_DEFAULT_SEC_GROUP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_instance",
                "aws_launch_template",
            } and (report := _use_default_security_group(graph, nid)):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f177.ec2_using_default_security_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
