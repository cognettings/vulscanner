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


def _kms_danger_key_rotation(graph: Graph, nid: NId) -> NId | None:
    en_key_rot, en_key_rot_val, en_key_rot_id = get_attribute(
        graph, nid, "enable_key_rotation"
    )
    key_spec, key_spec_val, _ = get_attribute(
        graph, nid, "customer_master_key_spec"
    )
    if key_spec and key_spec_val != "SYMMETRIC_DEFAULT":
        return None
    if not en_key_rot:
        return nid
    if en_key_rot_val in {"false", "0"}:
        return en_key_rot_id
    return None


def tfm_kms_key_is_key_rotation_absent_or_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_KMS_KEY_ROTATION_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_kms_key" and (
                report := _kms_danger_key_rotation(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=(
            "src.lib_path.f396.tfm_kms_key_is_key_rotation_absent_or_disabled"
        ),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
