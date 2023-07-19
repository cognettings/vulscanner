from collections.abc import (
    Iterator,
)
import json
from lib.root.f031.utils import (
    action_has_full_access_to_ssm,
    is_s3_action_writeable,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_attribute,
    get_key_value,
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
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils.aws_iam import (
    is_action_permissive,
    is_public_principal,
    is_resource_permissive,
)
from utils.function import (
    get_dict_values,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
    matching_nodes,
)

ELEVATED_POLICIES = {
    "PowerUserAccess",
    "IAMFullAccess",
    "AdministratorAccess",
}


def _iam_excessive_privileges(graph: Graph, nid: NId) -> NId | None:
    if (
        (pol_arns := get_optional_attribute(graph, nid, "managed_policy_arns"))
        and (value_id := graph.nodes[pol_arns[2]]["value_id"])
        and graph.nodes[value_id]["label_type"] == "ArrayInitializer"
    ):
        for array_elem in adj_ast(graph, value_id):
            value = graph.nodes[array_elem]["value"]
            if value.split("/")[-1] in ELEVATED_POLICIES:
                return array_elem
    return None


def _bucket_policy_allows_public_access_in_jsonencode(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if stmts := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[stmts[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            _, principal_val, _ = get_attribute(graph, c_id, "Principal")
            actions, _, action_id = get_attribute(graph, c_id, "Action")
            if actions:
                action_list = get_list_from_node(graph, action_id)
                if (
                    effect_val == "Allow"
                    and is_public_principal(principal_val)
                    and is_s3_action_writeable(action_list)
                ):
                    yield c_id


def is_wildcard_in_principals(graph: Graph, stmt: NId) -> bool:
    if (
        (principal := get_argument(graph, stmt, "principals"))
        and (types := get_optional_attribute(graph, principal, "type"))
        and (
            identifier := get_optional_attribute(
                graph, principal, "identifiers"
            )
        )
    ):
        identifier_list = get_list_from_node(graph, identifier[2])
        if types[1] == "*" and "*" in identifier_list:
            return True
    return False


def _bucket_policy_allows_public_access_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        effect, effect_val, _ = get_attribute(graph, stmt, "effect")
        action, _, action_id = get_attribute(graph, stmt, "actions")
        if action:
            action_list = get_list_from_node(graph, action_id)
            if (
                (effect_val == "Allow" or effect is None)
                and is_wildcard_in_principals(graph, stmt)
                and is_s3_action_writeable(action_list)
            ):
                yield stmt


def _aux_bucket_policy_public(attr_val: str, attr_id: NId) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        principal = stmt.get("Principal", "")
        actions = stmt.get("Action", [])
        if (
            effect == "Allow"
            and is_public_principal(principal)
            and is_s3_action_writeable(actions)
        ):
            yield attr_id


def _bucket_policy_allows_public_access(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _bucket_policy_allows_public_access_policy_resource(
            graph, nid
        )
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_bucket_policy_public(attr_val, attr_id)
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _bucket_policy_allows_public_access_in_jsonencode(
                    graph, value_id
                )


def _iam_has_full_access_to_ssm_in_jsonencode(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            actions, _, action_id = get_attribute(graph, c_id, "Action")
            if actions:
                action_list = get_list_from_node(graph, action_id)
                if effect_val == "Allow" and action_has_full_access_to_ssm(
                    action_list
                ):
                    yield c_id


def _iam_has_full_access_to_ssm_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        effect, effect_val, _ = get_attribute(graph, stmt, "effect")
        action, _, action_id = get_attribute(graph, stmt, "actions")
        if action:
            action_list = get_list_from_node(graph, action_id)
            if (
                effect_val == "Allow" or effect is None
            ) and action_has_full_access_to_ssm(action_list):
                yield stmt


def _aux_iam_has_full_access_to_ssm(
    attr_val: str, attr_id: NId
) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        actions = stmt.get("Action", [])
        if effect == "Allow" and action_has_full_access_to_ssm(actions):
            yield attr_id


def _iam_has_full_access_to_ssm(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _iam_has_full_access_to_ssm_policy_resource(graph, nid)
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_iam_has_full_access_to_ssm(attr_val, attr_id)
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _iam_has_full_access_to_ssm_in_jsonencode(
                    graph, value_id
                )


def _negative_statement_in_jsonencode(graph: Graph, nid: NId) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    statements, _, stmt_id = get_attribute(graph, child_id, "Statement")
    if statements:
        value_id = graph.nodes[stmt_id]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            _, effect_val, _ = get_attribute(graph, c_id, "Effect")
            if effect_val == "Allow":
                actions, _, action_id = get_attribute(graph, c_id, "NotAction")
                resources, _, resources_id = get_attribute(
                    graph, c_id, "NotResource"
                )
                action_list = get_list_from_node(graph, action_id)
                resources_list = get_list_from_node(graph, resources_id)
                if (
                    actions and not any(map(is_action_permissive, action_list))
                ) or (
                    resources
                    and not any(map(is_resource_permissive, resources_list))
                ):
                    yield c_id


def _negative_statement_policy_resource(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in iter_statements_from_policy_document(graph, nid):
        effect, effect_val, _ = get_attribute(graph, stmt, "effect")
        if effect_val == "Allow" or effect is None:
            actions, _, action_id = get_attribute(graph, stmt, "not_actions")
            resources, _, resources_id = get_attribute(
                graph, stmt, "not_resources"
            )
            action_list = get_list_from_node(graph, action_id)
            resources_list = get_list_from_node(graph, resources_id)
            if (
                actions and not any(map(is_action_permissive, action_list))
            ) or (
                resources
                and not any(map(is_resource_permissive, resources_list))
            ):
                yield stmt


def _aux_negative_statement(attr_val: str, attr_id: NId) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    for stmt in statements if isinstance(statements, list) else []:
        effect = stmt.get("Effect")
        if effect == "Allow":
            actions = stmt.get("NotAction")
            resource = stmt.get("NotResource")
            if (actions and not any(map(is_action_permissive, actions))) or (
                resource and not any(map(is_resource_permissive, resource))
            ):
                yield attr_id


def _negative_statement(graph: Graph, nid: NId) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _negative_statement_policy_resource(graph, nid)
    else:
        attr, attr_val, attr_id = get_attribute(graph, nid, "policy")
        if attr:
            value_id = graph.nodes[attr_id]["value_id"]
            if graph.nodes[value_id]["label_type"] == "Literal":
                yield from _aux_negative_statement(attr_val, attr_id)
            elif (
                graph.nodes[value_id]["label_type"] == "MethodInvocation"
                and graph.nodes[value_id]["expression"] == "jsonencode"
            ):
                yield from _negative_statement_in_jsonencode(graph, value_id)


def action_has_attach_role(
    actions: str | list,
    resources: str | list,
    iam_role_names: list[str],
) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    resource_list = resources if isinstance(resources, list) else [resources]
    for action in actions_list:
        if action == "iam:Attach*" and any(
            res.startswith("arn:aws:iam")
            and ":role/" in res
            and re.split(":role/", res)[1] in iam_role_names
            for res in resource_list
        ):
            return True
    return False


def _iam_excessive_role_policy_in_jsonencode(
    graph: Graph,
    nid: NId,
    iam_role_names: list[str],
) -> Iterator[NId]:
    child_id = graph.nodes[nid]["arguments_id"]
    if statements := get_optional_attribute(graph, child_id, "Statement"):
        value_id = graph.nodes[statements[2]]["value_id"]
        for c_id in adj_ast(graph, value_id, label_type="Object"):
            if (
                (effect := get_optional_attribute(graph, c_id, "Effect"))
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
                if action_has_attach_role(
                    action_list, resources_list, iam_role_names
                ):
                    yield c_id


def _iam_excessive_role_policy_in_literal(
    attr_val: str,
    attr_id: NId,
    iam_role_names: list[str],
) -> Iterator[NId]:
    dict_value = json.loads(attr_val)
    statements = get_dict_values(dict_value, "Statement")
    if not isinstance(statements, list):
        return

    for stmt in statements:
        if (
            stmt.get("Effect") == "Allow"
            and (actions := stmt.get("Action"))
            and (resource := stmt.get("Resource"))
            and action_has_attach_role(actions, resource, iam_role_names)
        ):
            yield attr_id


def _iam_excessive_role_policy_document(
    graph: Graph,
    nid: NId,
    iam_role_names: list[str],
) -> Iterator[NId]:
    for stmt in match_ast_group_d(graph, nid, "Object"):
        if (
            graph.nodes[stmt].get("name") == "statement"
            and (
                not (effect := get_optional_attribute(graph, stmt, "effect"))
                or effect[1] == "Allow"
            )
            and (action := get_optional_attribute(graph, stmt, "actions"))
            and (resources := get_optional_attribute(graph, stmt, "resources"))
        ):
            action_list = get_list_from_node(graph, action[2])
            resources_list = get_list_from_node(graph, resources[2])
            if action_has_attach_role(
                action_list, resources_list, iam_role_names
            ):
                yield stmt


def _iam_excessive_role_policy(
    graph: Graph,
    nid: NId,
    iam_role_names: list[str],
) -> Iterator[NId]:
    if graph.nodes[nid]["name"] == "aws_iam_policy_document":
        yield from _iam_excessive_role_policy_document(
            graph, nid, iam_role_names
        )
    elif attr := get_optional_attribute(graph, nid, "policy"):
        value_id = graph.nodes[attr[2]]["value_id"]
        if graph.nodes[value_id]["label_type"] == "Literal":
            yield from _iam_excessive_role_policy_in_literal(
                attr[1], attr[2], iam_role_names
            )
        elif (
            graph.nodes[value_id]["label_type"] == "MethodInvocation"
            and graph.nodes[value_id]["expression"] == "jsonencode"
        ):
            yield from _iam_excessive_role_policy_in_jsonencode(
                graph, value_id, iam_role_names
            )


def _get_managed_policy_arns(graph: Graph) -> list[str]:
    policy_arns = []
    for nid in matching_nodes(graph, label_type="Object"):
        if (name := graph.nodes[nid].get("name")) and name in {
            "aws_iam_group_policy_attachment",
            "aws_iam_policy_attachment",
            "aws_iam_role_policy_attachment",
            "aws_iam_user_policy_attachment",
        }:
            for attr_id in adj_ast(graph, nid, label_type="Pair"):
                _, value = get_key_value(graph, attr_id)
                if value.startswith("aws_iam_role."):
                    policy_arns.append(value.split(".")[1])
    return policy_arns


def _get_iam_role_names(graph: Graph) -> list[str]:
    policy_arns = _get_managed_policy_arns(graph)
    role_refnames = [
        "*",
    ]
    for nid in matching_nodes(graph, label_type="Object"):
        if (
            graph.nodes[nid].get("name") == "aws_iam_role"
            and (res_name := graph.nodes[nid]["tf_reference"].split(".")[1])
            and res_name in policy_arns
            and (name_attr := get_optional_attribute(graph, nid, "name"))
        ):
            role_refnames.append(name_attr[1])
    return role_refnames


def tfm_iam_excessive_role_policy(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_EXCESSIVE_ROLE_POLICY

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
                for report in _iam_excessive_role_policy(
                    graph,
                    nid,
                    _get_iam_role_names(graph),
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_excessive_role_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_negative_statement(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_NEGATIVE_STATEMENT

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
                for report in _negative_statement(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.negative_statement",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_has_full_access_to_ssm(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_FULL_ACCESS_SSM

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
                for report in _iam_has_full_access_to_ssm(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_bucket_policy_allows_public_access(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_BUCKET_ALLOWS_PUBLIC

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
                for report in _bucket_policy_allows_public_access(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.bucket_policy_allows_public_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_admin_policy_attached(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ADMIN_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                graph.nodes[nid].get("name")
                in {
                    "aws_iam_group_policy_attachment",
                    "aws_iam_policy_attachment",
                    "aws_iam_role_policy_attachment",
                    "aws_iam_user_policy_attachment",
                }
                and (
                    policy := get_optional_attribute(graph, nid, "policy_arn")
                )
                and policy[1].split("/")[-1] in ELEVATED_POLICIES
            ):
                yield shard, policy[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_user_missing_role_based_security(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_IAM_MISSING_SECURITY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_iam_user_policy" and (
                report := get_optional_attribute(graph, nid, "name")
            ):
                yield shard, report[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_user_missing_role_based_security",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_iam_excessive_privileges(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TFM_ADMIN_MANAGED_POLICIES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "aws_iam_role" and (
                report := _iam_excessive_privileges(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
