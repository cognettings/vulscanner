from collections.abc import (
    Iterator,
)
from lib.root.f325.utils import (
    has_attribute_wildcard,
    has_write_actions,
)
from lib.root.utilities.cloudformation import (
    get_attribute,
    get_list_from_node,
    get_optional_attribute,
    iterate_iam_policy_resources,
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
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils.aws_iam import (
    is_action_permissive,
    is_resource_permissive,
)
from utils.graph import (
    adj_ast,
)

WILDCARD_ACTION: re.Pattern = re.compile(r"^((\*)|(\w+:\*))$")
MANAGED_POLICIES = {
    "AWS::IAM::ManagedPolicy",
    "AWS::IAM::Policy",
    "AWS::IAM::Role",
    "AWS::IAM::User",
}


def _permissive_policy(graph: Graph, nid: NId) -> Iterator[NId]:
    if get_optional_attribute(
        graph, nid, "Condition"
    ) or get_optional_attribute(graph, nid, "Principal"):
        return

    if (
        (
            not (effect := get_optional_attribute(graph, nid, "Effect"))
            or effect[1] == "Allow"
        )
        and (action := get_optional_attribute(graph, nid, "Action"))
        and (resource := get_optional_attribute(graph, nid, "Resource"))
    ):
        action_list = get_list_from_node(graph, action[2])
        resources_list = get_list_from_node(graph, resource[2])
        if all(
            (
                any(map(is_action_permissive, action_list)),
                any(map(is_resource_permissive, resources_list)),
            )
        ):
            yield resource[2]


def _kms_key_has_master_keys_exposed_to_everyone(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if document := get_optional_attribute(graph, val_id, "KeyPolicy"):
        for stmt in yield_statements_from_policy(
            graph, graph.nodes[document[2]]["value_id"]
        ):
            effect, effect_val, _ = get_attribute(graph, stmt, "Effect")
            principal, _, p_id = get_attribute(graph, stmt, "Principal")
            if effect and effect_val == "Allow" and principal:
                p_attrs = graph.nodes[p_id].get("value_id")
                if (
                    p_attrs
                    and (aws := get_attribute(graph, p_attrs, "AWS"))
                    and aws[1] == "*"
                ):
                    yield aws[2]


def _action_list_has_wildcard(action_list: list) -> bool:
    wildcard_pattern = re.compile(r"^((\*)|(\w+:\*))$")
    for act in action_list:
        if wildcard_pattern.match(act):
            return True
    return False


def _aux_iam_allow_wildcard_actions(
    graph: Graph, policy_id: NId
) -> Iterator[NId]:
    if (
        (effect := get_optional_attribute(graph, policy_id, "Effect"))
        and effect[1] == "Allow"
        and (action := get_optional_attribute(graph, policy_id, "Action"))
        and (action_list := get_list_from_node(graph, action[2]))
        and _action_list_has_wildcard(action_list)
    ):
        yield action[2]


def _iam_allow_wildcard_action_trust_policy(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if document := get_optional_attribute(
        graph, val_id, "AssumeRolePolicyDocument"
    ):
        for stmt in yield_statements_from_policy(
            graph, graph.nodes[document[2]]["value_id"]
        ):
            yield from _aux_iam_allow_wildcard_actions(graph, stmt)


def _iam_allow_wildcard_action_policy(graph: Graph, nid: NId) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if policies := get_optional_attribute(graph, val_id, "Policies"):
        for policy in adj_ast(graph, graph.nodes[policies[2]]["value_id"]):
            _, _, pd_id = get_attribute(graph, policy, "PolicyDocument")
            for stmt in yield_statements_from_policy(
                graph, graph.nodes[pd_id]["value_id"]
            ):
                yield from _aux_iam_allow_wildcard_actions(graph, stmt)

    if policies := get_optional_attribute(graph, val_id, "PolicyDocument"):
        for stmt in yield_statements_from_policy(
            graph, graph.nodes[policies[2]]["value_id"]
        ):
            yield from _aux_iam_allow_wildcard_actions(graph, stmt)


def _stmt_has_wildcard_resource_on_write_action(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    for stmt in yield_statements_from_policy(graph, nid):
        if not (
            (effect := get_optional_attribute(graph, stmt, "Effect"))
            and effect[1] == "Allow"
        ):
            continue

        if (action := get_optional_attribute(graph, stmt, "Action")) and (
            resource := get_optional_attribute(graph, stmt, "Resource")
        ):
            res_list = get_list_from_node(graph, resource[2])
            action_list = get_list_from_node(graph, action[2])
            if has_attribute_wildcard(res_list) and has_write_actions(
                action_list
            ):
                yield resource[2]


def _wildcard_res_on_write_action_trust_policies(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if document := get_optional_attribute(
        graph, val_id, "AssumeRolePolicyDocument"
    ):
        yield from _stmt_has_wildcard_resource_on_write_action(
            graph, graph.nodes[document[2]]["value_id"]
        )


def _iam_has_wildcard_resource_on_write_action(
    graph: Graph, nid: NId
) -> Iterator[NId]:
    _, _, prop_id = get_attribute(graph, nid, "Properties")
    val_id = graph.nodes[prop_id]["value_id"]
    if policies := get_optional_attribute(graph, val_id, "Policies"):
        for policy in adj_ast(graph, graph.nodes[policies[2]]["value_id"]):
            if pol_doc := get_optional_attribute(
                graph, policy, "PolicyDocument"
            ):
                yield from _stmt_has_wildcard_resource_on_write_action(
                    graph, graph.nodes[pol_doc[2]]["value_id"]
                )

    if policies := get_optional_attribute(graph, val_id, "PolicyDocument"):
        yield from _stmt_has_wildcard_resource_on_write_action(
            graph, graph.nodes[policies[2]]["value_id"]
        )


def cfn_iam_has_wildcard_resource_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_WILDCARD_RESOURCES

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in MANAGED_POLICIES:
                for report in _iam_has_wildcard_resource_on_write_action(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f325.iam_has_wildcard_resource_on_write_action"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_has_wildcard_resource_trust_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_WILDCARD_WRITE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in MANAGED_POLICIES:
                for report in _wildcard_res_on_write_action_trust_policies(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f325.iam_has_wildcard_resource_on_write_action"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_has_wildcard_action_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_PERMISSIONS_POLICY_WILDCARD_ACTIONS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in MANAGED_POLICIES:
                for report in _iam_allow_wildcard_action_policy(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f325.iam_allow_wilcard_actions_permissions_policy"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_has_wildcard_action_trust_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_IAM_TRUST_POLICY_WILDCARD_ACTION

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] in MANAGED_POLICIES:
                for report in _iam_allow_wildcard_action_trust_policy(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f325.iam_allow_wildcard_action_trust_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_iam_permissive_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_PERMISSIVE_POLICY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in iterate_iam_policy_resources(graph, method_supplies):
            for report in _permissive_policy(graph, nid):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f325.permissive_policy",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def cfn_kms_master_keys_exposed_to_everyone(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_KMS_MASTER_KEYS_EXPOSED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::KMS::Key":
                for report in _kms_key_has_master_keys_exposed_to_everyone(
                    graph, nid
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key=("f325.kms_key_has_master_keys_exposed_to_everyone"),
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
