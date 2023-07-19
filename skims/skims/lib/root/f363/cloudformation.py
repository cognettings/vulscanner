from collections.abc import (
    Iterator,
)
from lib.root.utilities.cloudformation import (
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


def _aux_insecure_generate_secret_string(
    graph: Graph, s_attrs: NId
) -> Iterator[NId]:
    exclude_chars = get_optional_attribute(graph, s_attrs, "ExcludeCharacters")
    if exclude_chars:
        for charset in (
            set("0123456789"),
            set("abcdefghijklmnopqrstuvwxyz"),
            set("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"),
        ):
            # Do not allow to entirely exclude one type of chars
            if all(char in exclude_chars[1] for char in charset):
                yield exclude_chars[2]

    req_each_type = get_optional_attribute(
        graph, s_attrs, "RequireEachIncludedType"
    )
    if req_each_type and req_each_type[1] == "false":
        yield req_each_type[2]

    pass_length = get_optional_attribute(graph, s_attrs, "PasswordLength")
    if pass_length and int(pass_length[1]) < 14:
        yield pass_length[2]


def _insecure_generate_secret_string(graph: Graph, nid: NId) -> Iterator[NId]:
    if (
        (props := get_optional_attribute(graph, nid, "Properties"))
        and (val_id := graph.nodes[props[2]]["value_id"])
        and (
            secret := get_optional_attribute(
                graph, val_id, "GenerateSecretString"
            )
        )
    ):
        s_attrs = graph.nodes[secret[2]]["value_id"]
        for attr in (
            "ExcludeLowercase",
            "ExcludeUppercase",
            "ExcludeNumbers",
            "ExcludePunctuation",
        ):
            if (
                attr_node := get_optional_attribute(graph, s_attrs, attr)
            ) and attr_node[1] == "true":
                yield attr_node[2]
        yield from _aux_insecure_generate_secret_string(graph, s_attrs)


def cfn_insecure_generate_secret_string(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CFN_INSEC_GEN_SECRET

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if (
                resource := get_optional_attribute(graph, nid, "Type")
            ) and resource[1] == "AWS::SecretsManager::Secret":
                for report in _insecure_generate_secret_string(graph, nid):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f363.insecure_generate_secret_string",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
