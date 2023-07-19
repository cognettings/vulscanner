from collections.abc import (
    Iterator,
)
from lib.root.f052.common import (
    insec_msg_auth_mechanism,
    insecure_create_cipher,
    insecure_ec_keypair,
    insecure_ecdh_key,
    insecure_encrypt,
    insecure_hash,
    insecure_hash_library,
    insecure_rsa_keypair,
    jwt_insec_sign_async,
    jwt_insecure_sign,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def typescript_insecure_create_cipher(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_CREATE_CIPHER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in insecure_create_cipher(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_hash(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_HASH

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in insecure_hash(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_encrypt(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_ENCRYPT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in insecure_encrypt(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_ecdh_key(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_ECDH_KEY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in insecure_ecdh_key(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.TS_INSECURE_ECDH_KEY,
    )


def typescript_insecure_rsa_keypair(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_RSA_KEYPAIR

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in insecure_rsa_keypair(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_ec_keypair(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSECURE_EC_KEYPAIR

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in insecure_ec_keypair(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_key.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insecure_hash_library(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.JS_INSECURE_HASH_LIBRARY

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in insecure_hash_library(graph, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_jwt_insec_sign_algorithm(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_JWT_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in jwt_insecure_sign(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_jwt_insec_sign_algo_async(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_JWT_INSEC_SIGN_ALGO_ASYNC

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in jwt_insec_sign_async(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def typescript_insec_msg_auth_mechanism(
    shard: GraphShard,
    method_supplies: MethodSupplies,
) -> Vulnerabilities:
    method = MethodsEnum.TS_INSEC_MSG_AUTH_MECHANISM

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for n_id in insec_msg_auth_mechanism(graph, method, method_supplies):
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.insec_message_auth_mechanism",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
