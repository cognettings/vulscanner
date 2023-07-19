from collections.abc import (
    Iterator,
)
import json
from lib.root.f325.utils import (
    policy_has_excessive_permissions,
    policy_has_excessive_permissions_json_encode,
    policy_has_excessive_permissions_policy_document,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_attr_inside_attrs,
    get_list_from_node,
    get_optional_attribute,
    iter_statements_from_policy_document,
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
from utils.aws_iam import (
    is_action_permissive,
    is_resource_permissive,
)
from utils.function import (
    get_dict_values,
)
from utils.graph import (
    adj_ast,
)


def _kms_key_exposed_in_jsonencode(graph: Graph, nid: NId) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if stmt := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[stmt[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            if (
                (effect := get_optional_attribute(graph, c_id, "Effect"))
                and effect[1] == "Allow"
                and (
                    aws := get_attr_inside_attrs(
                        graph, c_id, ["Principal", "AWS"]
                    )
                )
                and aws[1] == "*"
            ):
                yield aws[2]


def _kms_key_exposed_in_literal(attr_val: str, attr_id: NId) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        aws = get_dict_values(stmt, "Principal", "AWS")
        if effect == "Allow" and aws and aws == "*":
            yield attr_id


def _kms_key_keys_exposed(graph: Graph, nid: NId) -> Iterator[NId]:
    if attr := get_optional_attribute(graph, nid, "policy"):
        value_id = graph.nodes[attr[2]]["value_id"]
        if graph.nodes[value_id]["label_type"] == "Literal":
            yield from _kms_key_exposed_in_literal(attr[1], attr[2])
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _kms_key_exposed_in_jsonencode(graph, value_id)


def _has_wildcard_on_policy_document(graph: Graph, nid: NId) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        if policy_has_excessive_permissions_policy_document(graph, stmt):
            yield stmt


def _has_wildcard_on_policy_in_literal(attr_val: str) -> bool:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        if policy_has_excessive_permissions(stmt):
            return True
    return False


def _has_wildcard_on_policy_in_jsonencode(
    graph: Graph,
    nid: NId,
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if stmt := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[stmt[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            if policy_has_excessive_permissions_json_encode(graph, c_id):
                yield c_id


def _iam_wildcard_on_trust_policy(graph: Graph, nid: NId) -> Iterator[NId]:
    if attr := get_optional_attribute(graph, nid, "assume_role_policy"):
        value_id = graph.nodes[attr[2]]["value_id"]
        if graph.nodes[value_id][
            "label_type"
        ] == "Literal" and _has_wildcard_on_policy_in_literal(attr[1]):
            yield attr[2]
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _has_wildcard_on_policy_in_jsonencode(graph, value_id)


def _iam_has_wildcard_on_action_or_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _has_wildcard_on_policy_document(graph, nid)
    elif attr := get_optional_attribute(graph, nid, "policy"):
        value_id = graph.nodes[attr[2]]["value_id"]
        if graph.nodes[value_id][
            "label_type"
        ] == "Literal" and _has_wildcard_on_policy_in_literal(attr[1]):
            yield attr[2]
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _has_wildcard_on_policy_in_jsonencode(graph, value_id)


def _permissive_policy_in_document(graph: Graph, nid: NId) -> Iterator[NId]:
    if get_argument(graph, nid, "condition") or get_argument(
        graph, nid, "principals"
    ):
        return

    for stmt in iter_statements_from_policy_document(graph, nid):
        if (
            (
                not (effect := get_optional_attribute(graph, stmt, "effect"))
                or effect[1] == "Allow"
            )
            and (action := get_optional_attribute(graph, stmt, "actions"))
            and (resources := get_optional_attribute(graph, stmt, "resources"))
        ):
            action_list = get_list_from_node(graph, action[2])
            resources_list = get_list_from_node(graph, resources[2])
            if all(
                (
                    any(map(is_action_permissive, action_list)),
                    any(map(is_resource_permissive, resources_list)),
                )
            ):
                yield stmt


def _permissive_policy_in_literal(
    attr_val: str,
    attr_id: NId,
) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        principal = stmt.get("Principal")
        condition = stmt.get("Condition")
        if effect == "Allow" and not principal and not condition:
            actions = stmt.get("Action", [])
            resource = stmt.get("Resource", [])
            if isinstance(actions, str):
                actions = [actions]
            if isinstance(resource, str):
                resource = [resource]
            if all(
                (
                    any(map(is_action_permissive, actions)),
                    any(map(is_resource_permissive, resource)),
                )
            ):
                yield attr_id


def _permissive_policy_in_jsonencode(graph: Graph, nid: NId) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if stmt := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[stmt[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            if get_argument(graph, c_id, "Principal") or get_argument(
                graph, c_id, "Condition"
            ):
                continue
            effect = get_optional_attribute(graph, c_id, "Effect")
            if (
                effect
                and effect[1] == "Allow"
                and (action := get_optional_attribute(graph, c_id, "Action"))
                and (
                    resources := get_optional_attribute(
                        graph, c_id, "Resource"
                    )
                )
            ):
                action_list = get_list_from_node(graph, action[2])
                resources_list = get_list_from_node(graph, resources[2])
                if all(
                    (
                        any(map(is_action_permissive, action_list)),
                        any(map(is_resource_permissive, resources_list)),
                    )
                ):
                    yield c_id


def _permissive_policy(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _permissive_policy_in_document(graph, nid)
    elif attr := get_optional_attribute(graph, nid, "policy"):
        value_id = graph.nodes[attr[2]]["value_id"]
        if graph.nodes[value_id]["label_type"] == "Literal":
            yield from _permissive_policy_in_literal(attr[1], attr[2])
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _permissive_policy_in_jsonencode(graph, value_id)


def tfm_iam_has_wildcard_on_trust_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_TRUST_POLICY_WILDCARD_ACTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_iam_role":
                for report in _iam_wildcard_on_trust_policy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f325.iam_allow_wildcard_action_trust_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_has_wildcard_on_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_WILDCARD_WRITE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_iam_group_policy",
                "aws_iam_policy",
                "aws_iam_role_policy",
                "aws_iam_user_policy",
                "aws_iam_policy_document",
            }:
                for report in _iam_has_wildcard_on_action_or_resource(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f325.iam_has_wildcard_resource_on_write_action",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_permissive_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_PERMISSIVE_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") in {
                "aws_iam_group_policy",
                "aws_iam_policy",
                "aws_iam_role_policy",
                "aws_iam_user_policy",
                "aws_iam_policy_document",
            }:
                for report in _permissive_policy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f325.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_kms_master_keys_exposed_to_everyone(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_KMS_MASTER_KEYS_EXPOSED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_kms_key":
                for report in _kms_key_keys_exposed(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f325.kms_key_has_master_keys_exposed_to_everyone"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
