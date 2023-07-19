from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
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
    match_ast_d,
)


def _ec2_use_default_security_group(graph: Graph, nid: NId) -> NId | None:
    prop = get_optional_attribute(graph, nid, "Properties")
    if not prop:
        return None

    val_id = graph.nodes[prop[2]]["value_id"]
    data_id = val_id
    report_id = prop[2]

    if launch_data := get_optional_attribute(
        graph, val_id, "LaunchTemplateData"
    ):
        data_id = graph.nodes[launch_data[2]]["value_id"]
        report_id = launch_data[2]

    if (
        (net_int := get_optional_attribute(graph, val_id, "NetworkInterfaces"))
        and (net_val_id := graph.nodes[net_int[2]]["value_id"])
        and graph.nodes[net_val_id]["label_type"] == "ArrayInitializer"
        and (obj_id := match_ast_d(graph, net_val_id, "Object"))
    ):
        if get_optional_attribute(graph, obj_id, "GroupSet"):
            return None
        return net_int[2]

    if not (
        get_optional_attribute(graph, data_id, "SecurityGroups")
        or get_optional_attribute(graph, data_id, "SecurityGroupIds")
    ):
        return report_id

    return None


def cfn_ec2_use_default_security_group(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_DEFAULT_SEC_GROUP

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1]
                in {
                    "AWS::EC2::LaunchTemplate",
                    "AWS::EC2::Instance",
                }
                and (report := _ec2_use_default_security_group(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f177.ec2_using_default_security_group",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
