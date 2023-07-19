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
    match_ast_group_d,
)


def _iam_role_is_over_privileged_in_jsonencode(
    graph: Graph, nid: NId, danger_attr: str
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if stmt := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[stmt[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            if (
                (effect := get_optional_attribute(graph, c_id, "Effect"))
                and effect[1] == "Allow"
                and (
                    not_princ := get_optional_attribute(
                        graph, c_id, danger_attr
                    )
                )
            ):
                yield not_princ[2]


def _iam_role_is_over_privileged_in_literal(
    policy_dict: str, danger_attr: str
) -> bool:
    dict_value = json.loads(policy_dict)
    statements = get_dict_values(dict_value, "Statement")
    if isinstance(statements, list):
        for stmt in statements:
            if stmt.get("Effect") == "Allow" and stmt.get(danger_attr):
                return True
    return False


def _iam_role_is_over_privileged(
    graph: Graph, nid: NId, danger_attr: str
) -> Iterator[NId]:
    if attr := get_optional_attribute(graph, nid, "assume_role_policy"):
        value_id = graph.nodes[attr[2]]["value_id"]
        if graph.nodes[value_id][
            "label_type"
        ] == "Literal" and _iam_role_is_over_privileged_in_literal(
            attr[1], danger_attr
        ):
            yield attr[2]
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _iam_role_is_over_privileged_in_jsonencode(
                graph, value_id, danger_attr
            )


def tfm_iam_allow_not_principal_trust_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_TRUST_POLICY_NOT_PRINCIPAL

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_iam_role":
                for report in _iam_role_is_over_privileged(
                    graph, nid, "NotPrincipal"
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_principal_trust_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_allow_not_actions_trust_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_TRUST_POLICY_NOT_ACTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_iam_role":
                for report in _iam_role_is_over_privileged(
                    graph, nid, "NotAction"
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_action_trust_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def _search_policy_in_jsonencode(
    graph: Graph, nid: NId, danger_el: str
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if statements := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[statements[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            if (
                (effect := get_optional_attribute(graph, c_id, "Effect"))
                and effect[1] == "Allow"
                and (d_attr := get_optional_attribute(graph, c_id, danger_el))
            ):
                yield d_attr[2]


def _search_policy_in_literal(
    attr_val: str,
    danger_el: str,
) -> bool:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    if isinstance(statements, list):
        for stmt in statements:
            if stmt.get("Effect") == "Allow" and stmt.get(danger_el):
                return True
    return False


def _search_policy_document(
    graph: Graph, nid: NId, danger_el: str
) -> Iterator[NId]:
    for stmt in match_ast_group_d(graph, nid, "Object"):
        if (
            graph.nodes[stmt].get("name") == "statement"
            and (
                not (effect := get_optional_attribute(graph, stmt, "effect"))
                or effect[1] == "Allow"
            )
            and (danger_attr := get_optional_attribute(graph, stmt, danger_el))
        ):
            yield danger_attr[2]


def _iam_search_danger_vals_in_policies(
    graph: Graph,
    nid: NId,
    danger_vals: tuple[str, str],
) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _search_policy_document(graph, nid, danger_vals[0])
    elif attr := get_optional_attribute(graph, nid, "policy"):
        value_id = graph.nodes[attr[2]]["value_id"]
        if graph.nodes[value_id][
            "label_type"
        ] == "Literal" and _search_policy_in_literal(attr[1], danger_vals[1]):
            yield attr[2]
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _search_policy_in_jsonencode(
                graph, value_id, danger_vals[1]
            )


def tfm_iam_allow_not_resource_perms_policies(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_PERMISSIONS_POLICY_NOT_RESOURCE

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
                for report in _iam_search_danger_vals_in_policies(
                    graph, nid, ("not_resources", "NotResource")
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_resourse_permissions_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_allow_not_action_perms_policies(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_PERMISSIONS_POLICY_NOT_ACTION

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
                for report in _iam_search_danger_vals_in_policies(
                    graph, nid, ("not_actions", "NotAction")
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_action_permissions_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_is_policy_applying_to_users(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_POLICY_APPLY_TO_USERS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name") == "aws_iam_user_policy"
                and get_optional_attribute(graph, nid, "policy")
                and (user := get_optional_attribute(graph, nid, "user"))
            ):
                yield shard, user[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_policies_applying_to_users",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
