from collections.abc import (
    Iterator,
)
from lib.path.common import (
    FALSE_OPTIONS,
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


def _kms_danger_key_rotation(graph: Graph, nid: NId) -> NId | None:
    props = get_optional_attribute(graph, nid, "Properties")
    if not props:
        return None
    val_id = graph.nodes[props[2]]["value_id"]
    key_spec = get_optional_attribute(graph, val_id, "KeySpec")
    if key_spec is None or key_spec[1] == "SYMMETRIC_DEFAULT":
        if not (
            key_rot := get_optional_attribute(
                graph, val_id, "EnableKeyRotation"
            )
        ):
            return props[2]
        if key_rot[1] in FALSE_OPTIONS:
            return key_rot[2]
    return None


def cfn_kms_key_is_key_rotation_absent_or_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_KMS_KEY_ROTATION_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1] == "AWS::KMS::Key"
                and (report := _kms_danger_key_rotation(graph, nid))
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "src.lib_path.f396.kms_key_is_key_rotation_absent_or_disabled"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
