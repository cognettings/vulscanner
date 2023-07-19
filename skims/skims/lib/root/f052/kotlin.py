from collections.abc import (
    Iterator,
)
from lib.root.utilities.kotlin import (
    check_method_origin,
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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
import utils.graph as g
from utils.string import (
    complete_attrs_on_set,
)


def kotlin_insecure_hash(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    danger_methods = complete_attrs_on_set(
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

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if n_attrs["expression"] in danger_methods:
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.KT_INSECURE_HASH,
    )


def kotlin_insecure_hash_instance(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_HASH
    danger_methods = complete_attrs_on_set(
        {
            "java.security.MessageDigest.getInstance",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                and get_node_evaluation_results(method, graph, arg_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_cipher(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_CIPHER
    danger_methods = complete_attrs_on_set(
        {
            "javax.crypto.Cipher.getInstance",
            "javax.crypto.KeyGenerator.getInstance",
            "javax.crypto.KeyPairGenerator.getInstance",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                and get_node_evaluation_results(method, graph, arg_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_cipher_ssl(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_CIPHER_SSL
    danger_methods = complete_attrs_on_set(
        {"javax.net.ssl.SSLContext.getInstance"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                and get_node_evaluation_results(method, graph, arg_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_cipher_http(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_CIPHER_HTTP
    danger_methods = {"tlsVersions"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            m_names = graph.nodes[n_id]["expression"].split(".")
            if (
                m_names[-1] in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                and get_node_evaluation_results(method, graph, arg_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_key_rsa(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_KEY
    danger_methods = complete_attrs_on_set(
        {"security.spec.RSAKeyGenParameterSpec"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                and get_node_evaluation_results(method, graph, arg_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_key_ec(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_KEY_EC
    danger_methods = complete_attrs_on_set(
        {"security.spec.ECGenParameterSpec"}
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] in danger_methods
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and (arg_id := g.match_ast(graph, al_id).get("__0__"))
                and get_node_evaluation_results(method, graph, arg_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_init_vector(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_INIT_VECTOR
    danger_methods = {"GCMParameterSpec"}
    lib = "javax.crypto.spec"

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                check_method_origin(graph, lib, danger_methods, n_attrs)
                and (al_id := graph.nodes[n_id].get("arguments_id"))
                and (arg_id := g.match_ast(graph, al_id).get("__1__"))
                and get_node_evaluation_results(method, graph, arg_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.init_vector_is_hcoded",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def search_host_verifier(graph: Graph, n_id: NId) -> str | None:
    var = g.pred_ast(graph, n_id)[0]
    if (
        var
        and (label_type := graph.nodes[var].get("label_type"))
        and label_type == "VariableDeclaration"
    ):
        var_name = graph.nodes[var]["variable"]
        expression = g.matching_nodes(graph, expression=var_name)
        if (
            expression
            and graph.nodes[expression[0]]["member"] == "hostnameVerifier"
        ):
            return expression[0]
    return None


def kotlin_insecure_hostname_ver(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_HOST_VERIFICATION
    danger_methods = {"OkHttpClient.Builder"}
    lib = "okhttp3"

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if check_method_origin(graph, lib, danger_methods, n_attrs) and (
                verifier := search_host_verifier(graph, n_id)
            ):
                yield shard, verifier

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.insec_hostname_verifier",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kotlin_insecure_certification(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_CERTIFICATE_VALIDATION
    danger_set = {"TrustManager"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["member"] == "init"
                and (parent := g.pred_ast(graph, n_id)[0])
                and get_node_evaluation_results(
                    method, graph, parent, danger_set
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.insec_certificate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kt_insecure_key_generator(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_KEY_GEN

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            parent = g.pred_ast(graph, n_id)
            arg_list = graph.nodes[parent[0]].get("arguments_id")

            if (
                n_attrs["member"] == "init"
                and (child := g.adj_ast(graph, n_id)[0])
                and get_node_evaluation_results(method, graph, child, set())
                and arg_list
                and get_node_evaluation_results(method, graph, arg_list, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kt_insecure_key_pair_generator(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_KEY_PAIR_GEN

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            parent = g.pred_ast(graph, n_id)
            arg_list = graph.nodes[parent[0]].get("arguments_id")

            if (
                n_attrs["member"] == "initialize"
                and (child := g.adj_ast(graph, n_id)[0])
                and get_node_evaluation_results(method, graph, child, set())
                and arg_list
                and get_node_evaluation_results(method, graph, arg_list, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kt_insecure_parameter_spec(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_PARAMETER_SPEC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                n_attrs["expression"] == "IvParameterSpec"
                and (args_id := n_attrs.get("arguments_id"))
                and get_node_evaluation_results(method, graph, args_id, set())
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def insec_sql_database(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    n_attrs = graph.nodes[n_id]
    if (
        n_attrs["expression"] == "SQLiteDatabase.openOrCreateDatabase"
        and (args_id := n_attrs.get("arguments_id"))
        and (key := g.adj_ast(graph, args_id))
        and get_node_evaluation_results(method, graph, key[1], set())
    ):
        return True
    if (
        n_attrs["expression"] == "RealmConfiguration.Builder().encryptionKey"
        and (args_id := n_attrs.get("arguments_id"))
        and (key := g.adj_ast(graph, args_id))
        and get_node_evaluation_results(method, graph, key[0], set())
    ):
        return True
    return False


def kt_insecure_encription_key(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSECURE_ENCRIPTION_KEY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            if insec_sql_database(graph, n_id, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.encription_key_is_hcoded",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def kt_insec_sign_algorithm(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.KT_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in method_supplies.selected_nodes:
            if graph.nodes["expression"] == "Algorithm.HMAC256":
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
