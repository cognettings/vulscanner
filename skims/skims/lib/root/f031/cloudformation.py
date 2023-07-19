from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
    get_attribute,
    get_list_from_node,
    get_optional_attribute,
    iterate_iam_policy_resources,
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
    is_public_principal,
    is_resource_permissive,
)
from utils.graph import (
    adj_ast,
)


def _is_s3_action_writeable(actions_list: list) -> bool:
    action_start_with = [
        "Copy",
        "Create",
        "Delete",
        "Put",
        "Restore",
        "Update",
        "Upload",
        "Write",
    ]
    for action in actions_list:
        if any(action.startswith(f"s3:{atw}") for atw in action_start_with):
            return True
    return False


def _iam_user_missing_role_based_security(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    if (
        (properties := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[properties[2]]["value_id"])
        and (policies := get_optional_attribute(graph, val_id, "Policies"))
        and (pol_attrs_id := graph.nodes[policies[2]]["value_id"])
    ):
        for pol in adj_ast(graph, pol_attrs_id):
            if pol_name := get_optional_attribute(graph, pol, "PolicyName"):
                yield pol_name[2]


def _admin_policy_attached(graph: Graph, nid: NId) -> Iterator[NId]:
    elevated_policies = {
        "PowerUserAccess",
        "IAMFullAccess",
        "AdministratorAccess",
    }

    if (
        (properties := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[properties[2]]["value_id"])
        and (
            policies := get_optional_attribute(
                graph, val_id, "ManagedPolicyArns"
            )
        )
        and (pol_attrs_id := graph.nodes[policies[2]]["value_id"])
    ):
        for pol_id in adj_ast(graph, pol_attrs_id):
            value = graph.nodes[pol_id]["value"]
            if value.split("/")[-1] in elevated_policies:
                yield pol_id


def _iam_has_full_access_to_ssm(graph: Graph, nid: NId) -> Iterator[NId]:
    effect, effect_val, _ = get_attribute(graph, nid, "Effect")
    action, action_val, action_id = get_attribute(graph, nid, "Action")
    if effect and action and effect_val == "Allow":
        action_attrs = graph.nodes[action_id]["value_id"]
        if graph.nodes[action_attrs]["label_type"] == "ArrayInitializer":
            for act in adj_ast(graph, action_attrs):
                if graph.nodes[act]["value"] == "ssm:*":
                    yield act
        elif action_val == "ssm:*":
            yield action_id


def _negative_statement(graph: Graph, nid: NId) -> Iterator[NId]:
    effect, effect_val, _ = get_attribute(graph, nid, "Effect")
    action, _, action_id = get_attribute(graph, nid, "NotAction")
    resource, _, res_id = get_attribute(graph, nid, "NotResource")
    action_list = get_list_from_node(graph, action_id)
    res_list = get_list_from_node(graph, res_id)
    if effect and effect_val == "Allow":
        if action:
            yield from (
                action_id
                for act in action_list
                if not is_action_permissive(act)
            )

        if resource:
            yield from (
                res_id for res in res_list if not is_resource_permissive(res)
            )


def _bucket_policy_allows_public_access(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    effect, effect_val, _ = get_attribute(graph, nid, "Effect")
    _, _, action_id = get_attribute(graph, nid, "Action")
    _, _, principal_id = get_attribute(graph, nid, "Principal")
    action_list = get_list_from_node(graph, action_id)
    principal_list = get_list_from_node(graph, principal_id)
    if (
        effect
        and effect_val == "Allow"
        and _is_s3_action_writeable(action_list)
        and is_public_principal(principal_list)
    ):
        yield principal_id


def cfn_bucket_policy_allows_public_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_BUCKET_ALLOWS_PUBLIC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in iterate_iam_policy_resources(graph, method_supplies):
            for report in _bucket_policy_allows_public_access(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.bucket_policy_allows_public_access",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def action_has_attach_role(
    actions: str | list,
    resources: str | list,
) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    resource_list = resources if isinstance(resources, list) else [resources]
    for action in actions_list:
        if action == "iam:Attach*" and any(
            res.startswith("arn:aws:iam") and ":role/" in res
            for res in resource_list
        ):
            return True
    return False


def _iam_excessive_role_policy(graph: Graph, stmt: NId) -> Iterator[NId]:
    if (
        (effect := get_optional_attribute(graph, stmt, "Effect"))
        and effect[1] == "Allow"
        and (action := get_optional_attribute(graph, stmt, "Action"))
        and (resource := get_optional_attribute(graph, stmt, "Resource"))
    ):
        res_list = get_list_from_node(graph, resource[2])
        action_list = get_list_from_node(graph, action[2])
        if action_has_attach_role(action_list, res_list):
            yield stmt


def cfn_iam_excessive_role_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_EXCESSIVE_ROLE_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_iam_policy_resources(graph, method_supplies):
            for report in _iam_excessive_role_policy(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_excessive_role_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_negative_statement(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_NEGATIVE_STATEMENT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in iterate_iam_policy_resources(graph, method_supplies):
            for report in _negative_statement(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.negative_statement",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_has_full_access_to_ssm(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_FULL_ACCESS_SSM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in iterate_iam_policy_resources(graph, method_supplies):
            for report in _iam_has_full_access_to_ssm(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_has_full_access_to_ssm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_admin_policy_attached(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_ADMIN_POLICY_ATTACHED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in {
                "AWS::IAM::Group",
                "AWS::IAM::Role",
                "AWS::IAM::User",
            }:
                for report in _admin_policy_attached(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031_aws.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_user_missing_role_based_security(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_MISSING_SECURITY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::IAM::User":
                for report in _iam_user_missing_role_based_security(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f031.iam_user_missing_role_based_security",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
