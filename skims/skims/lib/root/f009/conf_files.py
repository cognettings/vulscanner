from collections.abc import (
    Iterator,
)
from lib.root.utilities.json import (
    get_key_value,
    is_parent,
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


def has_password(value: str) -> bool:
    regex_password = re.compile(r"Password=.*")
    for element in value.split(";"):
        if re.match(regex_password, element):
            return True
    return False


def correct_email(value: str) -> bool:
    regex_email = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    if re.fullmatch(regex_email, value):
        return True
    return False


def _sensitive_info_in_dotnet(
    graph: Graph, nid: NId, key_pair: str, value: str
) -> bool:
    correct_parents = ["OutlookServices"]
    if (
        key_pair == "Email"
        and correct_email(value)
        and is_parent(graph, nid, correct_parents)
    ):
        return True
    return False


def _sensitive_info_json(
    graph: Graph, nid: NId, key_pair: str, value: str
) -> bool:
    correct_parents = ["ConnectionStrings"]
    if (
        key_pair == "Claims"
        and has_password(value)
        and is_parent(graph, nid, correct_parents)
    ):
        return True
    return False


def _sensitive_key_in_json(key_pair: str, value: str) -> bool:
    key_smell = {
        "api_key",
        "current_key",
    }
    grammar = re.compile(r"[A-Za-z0-9]{5,}")
    if key_pair in key_smell and re.fullmatch(grammar, value):
        return True
    return False


def json_sensitive_key(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.SENSITIVE_KEY_JSON

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            key, value = get_key_value(graph, node)

            if _sensitive_key_in_json(key, value):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f009.sensitive_key_in_json_exposed",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def json_sensitive_info_in_dotnet(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.SENSITIVE_INFO_DOTNET_JSON

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            key, value = get_key_value(graph, node)

            if _sensitive_info_in_dotnet(graph, node, key, value):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f009.sensitive_key_in_json_exposed",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def json_sensitive_info(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.SENSITIVE_INFO_JSON

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            key, value = get_key_value(graph, node)

            if _sensitive_info_json(graph, node, key, value):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f009.sensitive_key_in_json_exposed",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
