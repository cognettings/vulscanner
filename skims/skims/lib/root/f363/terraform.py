from collections.abc import (
    Iterator,
)
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


def _insecure_generate_secret_string(graph: Graph, nid: NId) -> Iterator[NId]:
    for attr in (
        "exclude_lowercase",
        "exclude_uppercase",
        "exclude_numbers",
        "exclude_punctuation",
    ):
        if (
            attr_node := get_optional_attribute(graph, nid, attr)
        ) and attr_node[1] == "true":
            yield attr_node[2]

    if (
        req_types := get_optional_attribute(
            graph, nid, "require_each_included_type"
        )
    ) and req_types[1] == "false":
        yield req_types[2]

    if (
        pass_length := get_optional_attribute(graph, nid, "password_length")
    ) and int(pass_length[1]) < 14:
        yield pass_length[2]

    if excl_chars := get_optional_attribute(graph, nid, "exclude_characters"):
        for charset in (
            set("0123456789"),
            set("abcdefghijklmnopqrstuvwxyz"),
            set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"),
        ):
            if all(char in excl_chars[1] for char in charset):
                yield excl_chars[2]


def tfm_insecure_generate_secret_string(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INSEC_GEN_SECRET
    res_name = "aws_secretsmanager_random_password"

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == res_name:
                for report in _insecure_generate_secret_string(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f363.insecure_generate_secret_string",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
