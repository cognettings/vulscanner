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


def _ec2_has_not_termination_protection(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    launch_data, _, launch_id = get_attribute(
        graph, val_id, "LaunchTemplateData"
    )
    report_id = prop_id
    if launch_data:
        val_id = val_id = graph.nodes[launch_id]["value_id"]
        report_id = launch_id
    api_termination, api_termination_val, api_termination_id = get_attribute(
        graph, val_id, "DisableApiTermination"
    )
    if not api_termination:
        yield report_id
    elif api_termination_val in FALSE_OPTIONS:
        yield api_termination_id


def cfn_ec2_has_not_termination_protection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_EC2_NOT_TERMINATION_PROTEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in {
                "AWS::EC2::LaunchTemplate",
                "AWS::EC2::Instance",
            }:
                for report in _ec2_has_not_termination_protection(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("src.lib_path.f257.ec2_has_not_termination_protection"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
