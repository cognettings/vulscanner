from collections.abc import (
    Iterator,
)
from lib.root.utilities.common import (
    check_methods_expression,
    library_is_imported,
)
from lib.root.utilities.java import (
    concatenate_name,
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
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
import utils.graph as g
from utils.string import (
    complete_attrs_on_set,
)


def get_eval_danger(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(
            method, graph, path, n_id, method_supplies.graph_db
        )
        if evaluation and evaluation.danger:
            return True
    return False


def java_insecure_pass(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    framework = "org.springframework.security"
    insecure_instances = complete_attrs_on_set(
        {
            f"{framework}.authentication.encoding.ShaPasswordEncoder",
            f"{framework}.authentication.encoding.Md5PasswordEncoder",
            f"{framework}.crypto.password.LdapShaPasswordEncoder",
            f"{framework}.crypto.password.Md4PasswordEncoder",
            f"{framework}.crypto.password.MessageDigestPasswordEncoder",
            f"{framework}.crypto.password.NoOpPasswordEncoder",
            f"{framework}.crypto.password.StandardPasswordEncoder",
            f"{framework}.crypto.scrypt.SCryptPasswordEncoder",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node]["name"] in insecure_instances:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_pass.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_PASS,
    )


def java_insecure_key_rsa(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_KEY_RSA
    insecure_rsa_spec = complete_attrs_on_set(
        {"java.security.spec.RSAKeyGenParameterSpec"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["name"] in insecure_rsa_spec
                and (al_id := n_attrs.get("arguments_id"))
                and (param := g.match_ast(graph, al_id).get("__0__"))
                and get_eval_danger(graph, param, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_key_ec(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_KEY_EC
    insecure_ec_spec = complete_attrs_on_set(
        {"java.security.spec.ECGenParameterSpec"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["name"] in insecure_ec_spec
                and (al_id := n_attrs.get("arguments_id"))
                and (param := g.match_ast(graph, al_id).get("__0__"))
                and get_eval_danger(graph, param, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_key_secret(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_KEY_SECRET
    insecure_secret_spec = complete_attrs_on_set(
        {"javax.crypto.spec.SecretKeySpec"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["name"] in insecure_secret_spec
                and (al_id := n_attrs.get("arguments_id"))
                and (childs := g.adj_ast(graph, al_id))
                and (param := childs[-1])
                and get_eval_danger(graph, param, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_hash(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    insecure_digests_1 = complete_attrs_on_set(
        {
            "org.apache.commons.codec.digest.DigestUtils.getMd2Digest",
            "org.apache.commons.codec.digest.DigestUtils.getMd5Digest",
            "org.apache.commons.codec.digest.DigestUtils.getShaDigest",
            "org.apache.commons.codec.digest.DigestUtils.getSha1Digest",
            "org.apache.commons.codec.digest.DigestUtils.md2",
            "org.apache.commons.codec.digest.DigestUtils.md2Hex",
            "org.apache.commons.codec.digest.DigestUtils.md5",
            "org.apache.commons.codec.digest.DigestUtils.md5Hex",
            "org.apache.commons.codec.digest.DigestUtils.sha",
            "org.apache.commons.codec.digest.DigestUtils.shaHex",
            "org.apache.commons.codec.digest.DigestUtils.sha1",
            "org.apache.commons.codec.digest.DigestUtils.sha1Hex",
            "com.google.common.hash.Hashing.adler32",
            "com.google.common.hash.Hashing.crc32",
            "com.google.common.hash.Hashing.crc32c",
            "com.google.common.hash.Hashing.goodFastHash",
            "com.google.common.hash.Hashing.hmacMd5",
            "com.google.common.hash.Hashing.hmacSha1",
            "com.google.common.hash.Hashing.md5",
            "com.google.common.hash.Hashing.sha1",
            "java.security.spec.MGF1ParameterSpec.SHA1",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            method_name = concatenate_name(graph, node)
            if method_name in insecure_digests_1:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_HASH,
    )


def java_insecure_hash_argument(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_HASH
    insecure_digests_2 = complete_attrs_on_set(
        {"java.security.MessageDigest.getInstance"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            method_name = concatenate_name(graph, node)
            n_attrs = graph.nodes[node]
            if (
                method_name in insecure_digests_2
                and (al_id := n_attrs.get("arguments_id"))
                and (param := g.match_ast(graph, al_id).get("__0__"))
                and get_eval_danger(graph, param, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_HASH,
    )


def java_insecure_cipher(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_CIPHER
    ciphers = complete_attrs_on_set(
        {
            "javax.crypto.Cipher.getInstance",
            "javax.crypto.KeyGenerator.getInstance",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            method_name = concatenate_name(graph, node)
            n_attrs = graph.nodes[node]
            if (
                method_name in ciphers
                and (al_id := n_attrs.get("arguments_id"))
                and (param := g.match_ast(graph, al_id).get("__0__"))
                and get_eval_danger(graph, param, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_cipher_ssl(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_CIPHER_SSL
    ssl_ciphers = complete_attrs_on_set(
        {"javax.net.ssl.SSLContext.getInstance"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            method_name = concatenate_name(graph, node)
            if (
                method_name in ssl_ciphers
                and (al_id := n_attrs.get("arguments_id"))
                and (param := g.match_ast(graph, al_id).get("__0__"))
                and get_eval_danger(graph, param, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_cipher_jmqi(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_CIPHER_JMQI
    jmqi_ciphers = complete_attrs_on_set(
        {
            "com.ibm.mq.jmqi.JmqiUtils.toCipherSuite",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            method_name = concatenate_name(graph, node)

            n_attrs = graph.nodes[node]
            if (
                method_name in jmqi_ciphers
                and (al_id := n_attrs.get("arguments_id"))
                and (param := g.match_ast(graph, al_id).get("__0__"))
                and get_eval_danger(graph, param, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def java_insecure_connection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_CONNECTION
    danger_method = {"tlsVersions"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if (
                check_methods_expression(graph, node, danger_method)
                and (args_id := graph.nodes[node].get("arguments_id"))
                and get_eval_danger(graph, args_id, method, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_connection.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_INSECURE_CONNECTION,
    )


def eval_danger_case(
    graph: Graph, method: MethodsEnum, dang_case: dict[str, str]
) -> set[NId]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        dang_exp = dang_case["dang_invocation"].split(".")[-1]

        return bool(
            (
                (node.get("label_type") == "MethodInvocation")
                and (node.get("expression") == dang_exp)
            )
            or (
                (node.get("label_type") == "ObjectCreation")
                and (node.get("name") == dang_exp)
            )
        )

    nodes = graph.nodes
    vuln_nodes: set[NId] = set()
    if not library_is_imported(graph, dang_case["dang_lib"]):
        return vuln_nodes
    for n_id in g.filter_nodes(graph, nodes, predicate_matcher):
        if (nodes[n_id].get("label_type") == "MethodInvocation") and (
            concatenate_name(graph, n_id) != dang_case["dang_invocation"]
        ):
            continue
        if (args_n_id := g.match_ast_d(graph, n_id, "ArgumentList")) and (
            get_node_evaluation_results(
                method, graph, args_n_id, {"hmacsha256"}, False
            )
        ):
            vuln_nodes.add(n_id)

    return vuln_nodes


def get_vuln_invocation_nodes(graph: Graph, method: MethodsEnum) -> set[NId]:
    vuln_nodes: set[NId] = set()
    dang_cases = [
        {"dang_lib": "javax.crypto.Mac", "dang_invocation": "Mac.getInstance"},
        {
            "dang_lib": "javax.crypto.spec.SecretKeySpec",
            "dang_invocation": "SecretKeySpec",
        },
    ]

    for dang_case in dang_cases:
        vuln_nodes.update(eval_danger_case(graph, method, dang_case))

    return vuln_nodes


def get_vuln_nodes_jwt(graph: Graph, method: MethodsEnum) -> set[NId]:
    vuln_nodes: set[NId] = set()
    vuln_nodes.update(get_vuln_invocation_nodes(graph, method))

    if not library_is_imported(graph, "io.jsonwebtoken.SignatureAlgorithm"):
        return vuln_nodes

    vuln_nodes.update(
        g.matching_nodes(
            graph, label_type="SymbolLookup", symbol="SignatureAlgorithm.HS256"
        )
    )
    return vuln_nodes


def java_insec_sign_algorithm(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.JAVA):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in get_vuln_nodes_jwt(graph, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
