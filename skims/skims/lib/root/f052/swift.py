from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib.root.utilities.common import (
    library_is_imported,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphDB,
    GraphShard,
    GraphShardMetadataLanguage as GraphLanguage,
    GraphShardNode,
    MethodSupplies,
    NId,
)
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
import utils.graph as g


def get_all_imports(graph: Graph) -> list[str]:
    return [
        graph.nodes[n_id]["expression"]
        for n_id in g.matching_nodes(
            graph,
            label_type="Import",
        )
    ]


def cc_algorithms(
    graph: Graph, ident: str, n_id: NId, file_imports: list[str]
) -> bool:
    if (
        ident == "CCAlgorithm"
        and "CommonCrypto" in file_imports
        and (args_id := graph.nodes[n_id].get("arguments_id"))
    ):
        arg = g.match_ast_d(graph, args_id, "SymbolLookup", 2)
        if graph.nodes[arg]["symbol"] == "kCCAlgorithmDES":
            return True
    return False


def swift_insecure_cipher(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    danger_methods = {
        ("Blowfish", "CryptoSwift"),
        (
            ".des",
            "IDZSwiftCommonCrypto",
        ),
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        file_imports = get_all_imports(graph)
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            ident = n_attrs.get("expression") or n_attrs.get("symbol")

            if any(
                meth == ident and imp in file_imports
                for meth, imp in danger_methods
            ) or cc_algorithms(graph, ident, n_id, file_imports):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Swift"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.SWIFT_INSECURE_CIPHER,
    )


def uses_des_algorithm(graph: Graph, n_id: NId) -> bool:
    named_args = g.match_ast_group_d(graph, n_id, "NamedArgument", 2)
    for arg in named_args:
        arg_name = graph.nodes[arg]["argument_name"]
        val_id = graph.nodes[arg]["value_id"]
        if arg_name == "algorithm" and graph.nodes[val_id]["symbol"] == ".des":
            return True
    return False


def swift_insecure_crypto(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    danger_methods = {"Cryptor"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            ident = n_attrs.get("expression")

            if ident in danger_methods and uses_des_algorithm(graph, n_id):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Swift"),
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.SWIFT_INSECURE_CRYPTOR,
    )


def swift_insecure_cryptalgo(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    danger_methods = {"CryptAlgorithm"}
    method = MethodsEnum.SWIFT_INSECURE_CRYPTOR

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            ident = n_attrs.get("expression")
            parent = g.pred_ast(graph, n_id)[0]
            var_id = graph.nodes[parent]["value_id"]
            if ident in danger_methods and get_node_evaluation_results(
                method, graph, var_id, set()
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params=dict(lang="Swift"),
        graph_shard_nodes=n_ids(),
        method=method,
    )


def get_cryptoswift_vulns(graph: Graph) -> set[NId]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        # REGEX provisional approach until SyntaxTree Enhancements done
        # See issue: 9366
        hmac_matcher = re.compile(
            r"HMAC\(.*variant:(?:\.sha256|\.sha1)[^)]*\)?"
        )
        return bool(
            node.get("label_type") == "MethodInvocation"
            and (exp := node.get("expression"))
            and (hmac_matcher.search(exp))
        )

    vuln_nodes: set[NId] = set()
    if not library_is_imported(graph, "CryptoSwift"):
        return vuln_nodes

    vuln_nodes.update(g.filter_nodes(graph, graph.nodes, predicate_matcher))

    return vuln_nodes


def get_cryptokit_vulns(graph: Graph) -> set[NId]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        dang_members = {"HMAC<SHA256>", "HMAC<Insecure.SHA1>"}
        return bool(node.get("label_type") == "MemberAccess") and (
            node.get("member") in dang_members
        )

    vuln_nodes = set()

    for n_id in g.filter_nodes(
        graph,
        graph.nodes,
        predicate_matcher,
    ):
        vuln_nodes.add(n_id)

    return vuln_nodes


def swift_insec_sign_algorithm(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.SWIFT_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.SWIFT):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph

            for n_id in chain(
                get_cryptokit_vulns(graph),
                get_cryptoswift_vulns(graph),
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
