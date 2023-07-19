from collections.abc import (
    Iterator,
)
import json
from lib.root.utilities.terraform import (
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
from utils.function import (
    get_dict_values,
)
from utils.graph import (
    adj_ast,
)


def _bucket_policy_in_jsonencode(graph: Graph, nid: NId) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if stmts := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[stmts[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            effect = get_optional_attribute(graph, c_id, "Effect")
            if (
                not effect
                or effect[1] != "Allow"
                or not (
                    condition := get_optional_attribute(
                        graph, c_id, "Condition"
                    )
                )
            ):
                continue

            c_val_id = graph.nodes[condition[2]]["value_id"]
            null = get_optional_attribute(graph, c_val_id, "Null")
            if (
                null
                and (n_val_id := graph.nodes[null[2]]["value_id"])
                and (
                    ss_enc := get_optional_attribute(
                        graph, n_val_id, "s3:x-amz-server-side-encryption"
                    )
                )
                and ss_enc[1] == "false"
            ):
                yield ss_enc[2]


def _bucket_policy_in_literal(attr_val: str, attr_id: NId) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    if not isinstance(statements, list):
        return

    for stmt in statements:
        effect = stmt.get("Effect")
        if effect != "Allow":
            continue

        if (
            (condition := stmt.get("Condition"))
            and (null := condition.get("Null"))
            and not null.get("s3:x-amz-server-side-encryption", True)
        ):
            yield attr_id


def _bucket_policy_ssenc_disabled(graph: Graph, nid: NId) -> Iterator[NId]:
    if policy := get_optional_attribute(graph, nid, "policy"):
        value_id = graph.nodes[policy[2]]["value_id"]
        if graph.nodes[value_id]["label_type"] == "Literal":
            yield from _bucket_policy_in_literal(policy[1], policy[2])
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _bucket_policy_in_jsonencode(graph, value_id)


def tfm_bucket_server_side_encryption_disabled(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_POLICY_SERVER_ENCRYP_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_s3_bucket_policy":
                for report in _bucket_policy_ssenc_disabled(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f099.s3_has_server_side_encryption_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
