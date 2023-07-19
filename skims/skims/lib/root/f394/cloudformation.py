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


def _log_files_not_validated(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    file_validation, file_val, file_id = get_attribute(
        graph, val_id, "EnableLogFileValidation"
    )
    if not file_validation:
        yield prop_id
    elif file_val in FALSE_OPTIONS:
        yield file_id


def cfn_log_files_not_validated(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_LOG_NOT_VALIDATED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::CloudTrail::Trail":
                for report in _log_files_not_validated(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f394.cfn_log_files_not_validated",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
