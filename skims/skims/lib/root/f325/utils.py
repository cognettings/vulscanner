from contextlib import (
    suppress,
)
from lib.root.utilities.terraform import (
    get_list_from_node,
    get_optional_attribute,
)
from model.graph import (
    Graph,
    NId,
)
import re
from utils.aws_iam import (
    ACTIONS,
)


def has_attribute_wildcard(attribute: str | list) -> bool:
    result = False
    for value in attribute if isinstance(attribute, list) else [attribute]:
        if value == "*":
            result = True
            break
    return result


def has_write_actions(actions: str | list) -> bool:
    result = False
    for entry in actions if isinstance(actions, list) else [actions]:
        with suppress(ValueError):
            service, action = entry.split(":")
            if service in ACTIONS:
                if (
                    "*" in action
                    and len(
                        [
                            act
                            for act in ACTIONS[service].get("write", [])
                            if re.match(action.replace("*", ".*"), act)
                            and act
                            not in ACTIONS[service].get(
                                "wildcard_resource", []
                            )
                        ]
                    )
                    > 0
                ):
                    result = True
                    break
                if action in ACTIONS[service].get(
                    "write", []
                ) and action not in ACTIONS[service].get(
                    "wildcard_resource", []
                ):
                    result = True
                    break
    return result


def policy_has_excessive_permissions(stmt: dict) -> bool:
    has_excessive_permissions = False
    if stmt.get("Effect") == "Allow":
        actions = stmt.get("Action", [])
        resource = stmt.get("Resource", [])
        if has_attribute_wildcard(resource) and (
            has_attribute_wildcard(actions) or has_write_actions(actions)
        ):
            has_excessive_permissions = True
    return has_excessive_permissions


def policy_has_excessive_permissions_policy_document(
    graph: Graph, stmt: NId
) -> bool:
    has_excessive_permissions = False
    if (
        (
            not (effect := get_optional_attribute(graph, stmt, "effect"))
            or effect[1] == "Allow"
        )
        and (actions := get_optional_attribute(graph, stmt, "actions"))
        and (resources := get_optional_attribute(graph, stmt, "resources"))
    ):
        action_list = get_list_from_node(graph, actions[2])
        resources_list = get_list_from_node(graph, resources[2])
        if has_attribute_wildcard(resources_list) and (
            has_attribute_wildcard(action_list)
            or has_write_actions(action_list)
        ):
            has_excessive_permissions = True
    return has_excessive_permissions


def policy_has_excessive_permissions_json_encode(
    graph: Graph, stmt: NId
) -> bool:
    has_excessive_permissions = False
    if (
        (
            not (effect := get_optional_attribute(graph, stmt, "effect"))
            or effect[1] == "Allow"
        )
        and (actions := get_optional_attribute(graph, stmt, "Action"))
        and (resources := get_optional_attribute(graph, stmt, "Resource"))
    ):
        action_list = get_list_from_node(graph, actions[2])
        resources_list = get_list_from_node(graph, resources[2])
        if has_attribute_wildcard(resources_list) and (
            has_attribute_wildcard(action_list)
            or has_write_actions(action_list)
        ):
            has_excessive_permissions = True
    return has_excessive_permissions
