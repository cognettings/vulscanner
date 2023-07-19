from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
    get_optional_attribute,
    yield_statements_from_policy,
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
    adj_ast,
)

AWS_ROLE = "AWS::IAM::Role"


def _iam_allow_not_element_trust_policy(
    graph: Graph,
    nid: NId,
    danger_element: str,
) -> Iterator[NId]:
    if (
        (props := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[props[2]]["value_id"])
        and (
            pol_doc := get_optional_attribute(
                graph, val_id, "AssumeRolePolicyDocument"
            )
        )
    ):
        for stmt in yield_statements_from_policy(
            graph, graph.nodes[pol_doc[2]]["value_id"]
        ):
            if (
                (effect := get_optional_attribute(graph, stmt, "Effect"))
                and effect[1] == "Allow"
                and (
                    danger_el := get_optional_attribute(
                        graph, stmt, danger_element
                    )
                )
            ):
                yield danger_el[2]


def _iam_allow_not_element_perms_policies(
    graph: Graph,
    nid: NId,
    danger_element: str,
) -> Iterator[NId]:
    if (
        (props := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[props[2]]["value_id"])
        and (pols := get_optional_attribute(graph, val_id, "Policies"))
    ):
        for policy in adj_ast(graph, graph.nodes[pols[2]]["value_id"]):
            if not (
                pol_doc := get_optional_attribute(
                    graph, policy, "PolicyDocument"
                )
            ):
                continue

            for stmt in yield_statements_from_policy(
                graph, graph.nodes[pol_doc[2]]["value_id"]
            ):
                if (
                    (effect := get_optional_attribute(graph, stmt, "Effect"))
                    and effect[1] == "Allow"
                    and (
                        danger_el := get_optional_attribute(
                            graph, stmt, danger_element
                        )
                    )
                ):
                    yield danger_el[2]


def cfn_iam_allow_not_resource_perms_policies(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_NOT_RESOURCE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == AWS_ROLE:
                for report in _iam_allow_not_element_perms_policies(
                    graph, nid, "NotResource"
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_resourse_permissions_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_allow_not_action_perms_policies(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_NOT_ACTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == AWS_ROLE:
                for report in _iam_allow_not_element_perms_policies(
                    graph, nid, "NotAction"
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_action_permissions_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_allow_not_principal_trust_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_PRINCIPAL

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == AWS_ROLE:
                for report in _iam_allow_not_element_trust_policy(
                    graph, nid, "NotPrincipal"
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_principal_trust_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_allow_not_actions_trust_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_NOT_ACTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == AWS_ROLE:
                for report in _iam_allow_not_element_trust_policy(
                    graph, nid, "NotAction"
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_allow_not_action_trust_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_is_policy_applying_to_users(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_POLICY_APPLY_TO_USERS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                (resource := get_optional_attribute(graph, nid, "Type"))
                and resource[1]
                in {"AWS::IAM::ManagedPolicy", "AWS::IAM::Policy"}
                and (props := get_optional_attribute(graph, nid, "Properties"))
                and (val_id := graph.nodes[props[2]]["value_id"])
                and get_optional_attribute(graph, val_id, "Users")
            ):
                yield shard, props[2]

    return get_vulnerabilities_from_n_ids(
        desc_key="f165.iam_policies_applying_to_users",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
