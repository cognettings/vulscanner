from collections.abc import (
    Iterator,
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
import utils.graph as g


def go_insecure_hash(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    danger_methods = {"md4", "md5", "ripemd160", "sha1"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["member"] in danger_methods
                and n_attrs["expression"] == "New"
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params=dict(lang="Go"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.GO_INSECURE_HASH,
    )


def go_insecure_cipher(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    danger_methods = {"des.NewTripleDESCipher", "blowfish.NewCipher"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if n_attrs["expression"] in danger_methods:
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Go"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.GO_INSECURE_CIPHER,
    )


def get_hs_vulns(
    graph: Graph, method_supplies: MethodSupplies
) -> tuple[NId, ...]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        dang_expressions = {"SigningMethodHS256", "MethodHS256", "HS256"}
        return bool(
            (node.get("member") == "jwt")
            and (node.get("expression") in dang_expressions)
        )

    return g.filter_nodes(
        graph, method_supplies.selected_nodes, predicate_matcher
    )


def go_insec_sign_algorithm(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.GO_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in get_hs_vulns(graph, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
