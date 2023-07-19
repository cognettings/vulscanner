from collections.abc import (
    Iterator,
)
from contextlib import (
    suppress,
)
from ipaddress import (
    AddressValueError,
    IPv4Network,
    IPv6Network,
)
from model.graph import (
    Graph,
    MethodSupplies,
    NId,
)
from utils.graph import (
    adj_ast,
    match_ast_group_d,
)


def is_cidr(cidr: str) -> bool:
    """Validate if a string is a valid CIDR."""
    result = False
    with suppress(AddressValueError, ValueError):
        IPv4Network(cidr, strict=False)
        result = True
    with suppress(AddressValueError, ValueError):
        IPv6Network(cidr, strict=False)
        result = True
    return result


def get_key_value(graph: Graph, nid: NId) -> tuple[str, str]:
    key_id = graph.nodes[nid]["key_id"]
    key = graph.nodes[key_id]["value"]
    value_id = graph.nodes[nid]["value_id"]
    value = ""
    if graph.nodes[value_id]["label_type"] == "ArrayInitializer":
        child_id = adj_ast(graph, value_id, label_type="Literal")
        if len(child_id) > 0:
            value = graph.nodes[child_id[0]].get("value", "")
    else:
        value = graph.nodes[value_id].get("value", "")
    return key, value


def get_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> tuple[str | None, str, NId]:
    if object_id != "":
        for attr_id in adj_ast(graph, object_id, label_type="Pair"):
            key, value = get_key_value(graph, attr_id)
            if key == expected_attr:
                return key, value, attr_id
    return None, "", ""


def get_optional_attribute(
    graph: Graph, object_id: NId, expected_attr: str
) -> tuple[str, str, NId] | None:
    """
    Search an optional attribute in an object node and, if found,
    return a tuple with [key_name, key_value, Node_Id]
    """
    for n_id in match_ast_group_d(graph, object_id, "Pair"):
        key, value = get_key_value(graph, n_id)
        if key == expected_attr:
            return key, value, n_id
    return None


def get_optional_attribute_inside_path(
    graph: Graph, nid: NId, attributes_path: list[str]
) -> tuple[str, str, NId] | None:
    """
    Search optional attributes nested inside one another.
    If the entire list is found, returns the last attribute node as a tuple
    [key_name, key_value, Node_Id]
    """
    curr_nid = nid
    for attribute in attributes_path:
        if not curr_nid:
            attr = None
            break
        attr = get_optional_attribute(graph, curr_nid, attribute)
        if not attr:
            break
        curr_nid = graph.nodes[attr[2]].get("value_id")
    return attr


def list_has_string(graph: Graph, nid: NId, value: str) -> bool:
    child_ids = adj_ast(graph, nid)
    for c_id in child_ids:
        curr_value = graph.nodes[c_id].get("value")
        if curr_value and curr_value == value:
            return True
    return False


def get_list_from_node(graph: Graph, nid: NId | None) -> list:
    if nid:
        value_id = graph.nodes[nid]["value_id"]
        if graph.nodes[value_id]["label_type"] == "ArrayInitializer":
            child_ids = adj_ast(graph, value_id)
            result: list = []
            for c_id in child_ids:
                result.append(graph.nodes[c_id].get("value"))
            return result
        return [graph.nodes[value_id].get("value")]
    return []


def yield_statements_from_policy(graph: Graph, nid: NId) -> Iterator[NId]:
    if stmt := get_optional_attribute(graph, nid, "Statement"):
        stmt_attrs = graph.nodes[stmt[2]]["value_id"]
        yield from adj_ast(graph, stmt_attrs)


def _aux_iterate_iam_policy_documents(
    graph: Graph, nid: NId, resource: str
) -> Iterator[NId]:
    if resource in {
        "AWS::IAM::ManagedPolicy",
        "AWS::IAM::Policy",
        "AWS::S3::BucketPolicy",
    } and (pol_doc := get_optional_attribute(graph, nid, "PolicyDocument")):
        yield from yield_statements_from_policy(
            graph, graph.nodes[pol_doc[2]]["value_id"]
        )

    if (
        resource in {"AWS::IAM::Role", "AWS::IAM::User"}
        and (policies := get_optional_attribute(graph, nid, "Policies"))
        and policies[0]
    ):
        for policy in adj_ast(graph, graph.nodes[policies[2]]["value_id"]):
            if pol_doc := get_optional_attribute(
                graph, policy, "PolicyDocument"
            ):
                yield from yield_statements_from_policy(
                    graph, graph.nodes[pol_doc[2]]["value_id"]
                )

    if resource == "AWS::IAM::Role" and (
        pol_doc := get_optional_attribute(
            graph, nid, "AssumeRolePolicyDocument"
        )
    ):
        yield from yield_statements_from_policy(
            graph, graph.nodes[pol_doc[2]]["value_id"]
        )


def iterate_iam_policy_resources(
    graph: Graph, method_supplies: MethodSupplies
) -> Iterator[NId]:
    policy_resources = {
        "AWS::IAM::ManagedPolicy",
        "AWS::IAM::Policy",
        "AWS::S3::BucketPolicy",
        "AWS::IAM::Role",
        "AWS::IAM::User",
    }
    for nid in method_supplies.selected_nodes:
        if (
            (res_type := get_optional_attribute(graph, nid, "Type"))
            and res_type[1] in policy_resources
            and (props := (get_optional_attribute(graph, nid, "Properties")))
            and (val_id := graph.nodes[props[2]]["value_id"])
        ):
            yield from _aux_iterate_iam_policy_documents(
                graph, val_id, res_type[1]
            )
