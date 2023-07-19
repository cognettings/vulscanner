from collections.abc import (
    Iterator,
)
from itertools import (
    chain,
)
from lib.root.f052.common import (
    CS_INSECURE_CIPHERS,
    CS_INSECURE_HASH,
)
from lib.root.utilities.c_sharp import (
    yield_syntax_graph_member_access,
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
    MetadataGraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
    get_vulnerabilities_from_n_ids_metadata,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
import utils.graph as g
from utils.string import (
    build_attr_paths,
)


def is_insecure_keys(
    graph: Graph, n_id: str, method_supplies: MethodSupplies
) -> bool:
    method = MethodsEnum.CS_INSECURE_KEYS
    n_attrs = graph.nodes[n_id]
    unsafe_method = "RSACryptoServiceProvider"

    if n_attrs["name"] == unsafe_method and is_rsa_insecure(graph, n_id):
        return True

    if (
        n_attrs["name"] in {"DSACng", "RSACng"}
        and (a_id := n_attrs.get("arguments_id"))
        and (test_nid := g.match_ast(graph, a_id).get("__0__"))
    ):
        return get_node_evaluation_results(
            method, graph, test_nid, set(), graph_db=method_supplies.graph_db
        )

    return False


def get_crypto_var_names(graph: Graph) -> list[NId]:
    name_vars = []
    for var_id in g.matching_nodes(graph, label_type="VariableDeclaration"):
        node_var = graph.nodes[var_id]
        if node_var.get("variable_type") == "RSACryptoServiceProvider":
            name_vars.append(graph.nodes[var_id].get("variable"))
    return name_vars


def get_mode_node(
    graph: Graph,
    members: tuple[str, ...],
    identifier: str,
) -> NId | None:
    test_node = None
    for member in members:
        if graph.nodes[member].get(identifier) == "Mode":
            test_node = graph.nodes[g.pred(graph, member)[0]].get("value_id")
    return test_node


def is_rsa_insecure(graph: Graph, n_id: NId) -> bool:
    method = MethodsEnum.CS_INSECURE_KEYS
    n_attrs = graph.nodes[n_id]
    a_id = n_attrs.get("arguments_id")

    if not a_id or (
        (test_nid := g.match_ast(graph, a_id).get("__0__"))
        and get_node_evaluation_results(method, graph, test_nid, set())
    ):
        return True
    return False


def is_managed_mode_insecure(
    graph: Graph, n_id: NId, method_supplies: MethodSupplies
) -> NId | None:
    method = MethodsEnum.CS_MANAGED_SECURE_MODE

    if g.match_ast_d(graph, n_id, "ExpressionStatement"):
        props = g.get_ast_childs(graph, n_id, "SymbolLookup", depth=3)
        test_nid = get_mode_node(graph, props, "symbol")
    else:
        parent_id = g.pred(graph, n_id)[0]
        var_name = graph.nodes[parent_id].get("variable")
        members = [*yield_syntax_graph_member_access(graph, var_name)]
        test_nid = get_mode_node(graph, tuple(members), "member")

    if test_nid and get_node_evaluation_results(
        method, graph, test_nid, set(), graph_db=method_supplies.graph_db
    ):
        return test_nid

    return None


def c_sharp_insecure_keys(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_KEYS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if is_insecure_keys(graph, node, method_supplies):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_rsa_secure_mode(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_RSA_SECURE_MODE

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        name_vars = get_crypto_var_names(graph)
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            parent_nid = g.pred(graph, node)[0]

            if (
                n_attrs["expression"] in name_vars
                and n_attrs.get("member") == "Encrypt"
                and (al_id := graph.nodes[parent_nid].get("arguments_id"))
                and (test_nid := g.match_ast(graph, al_id).get("__1__"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    test_nid,
                    set(),
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_managed_secure_mode(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    insecure_objects = {"AesManaged"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("name") in insecure_objects and (
                mode_nid := is_managed_mode_insecure(
                    graph, node, method_supplies
                )
            ):
                yield shard, mode_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_MANAGED_SECURE_MODE,
    )


def c_sharp_insecure_cipher_member_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("expression") in CS_INSECURE_CIPHERS:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_CIPHER,
    )


def c_sharp_insecure_cipher_object_creation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("name") in CS_INSECURE_CIPHERS:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_cipher.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_CIPHER,
    )


def c_sharp_insecure_hash_member_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("expression") in CS_INSECURE_HASH:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_HASH,
    )


def c_sharp_insecure_hash_object_creation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("name") in CS_INSECURE_HASH:
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_path.f052.insecure_hash.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_INSECURE_HASH,
    )


def c_sharp_disabled_strong_crypto(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_DISABLED_STRONG_CRYPTO
    rules = {"Switch.System.Net.DontEnableSchUseStrongCrypto", "true"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("expression") == "AppContext":
                test_nid = g.pred_ast(graph, node)[0]
                if graph.nodes[node][
                    "member"
                ] == "SetSwitch" and get_node_evaluation_results(
                    method,
                    graph,
                    test_nid,
                    rules,
                    graph_db=method_supplies.graph_db,
                ):
                    yield shard, test_nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.c_sharp_disabled_strong_crypto",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_obsolete_key_derivation_method_invocation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_OBSOLETE_KEY_DERIVATION
    possible_paths = build_attr_paths(
        "System",
        "Security",
        "Cryptography",
        "rfc2898DeriveBytes",
        "CryptDeriveKey",
    )

    def n_ids() -> Iterator[MetadataGraphShardNode]:
        metadata = {}
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (expr := n_attrs.get("expression")) and expr in possible_paths:
                metadata["desc_params"] = {"expression": expr}
                yield shard, node, metadata

    return get_vulnerabilities_from_n_ids_metadata(
        desc_key="lib_root.f052.c_sharp_obsolete_key_derivation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_obsolete_key_derivation_object_creation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_OBSOLETE_KEY_DERIVATION

    def n_ids() -> Iterator[MetadataGraphShardNode]:
        metadata = {}
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if n_attrs.get("name") == "PasswordDeriveBytes":
                metadata["desc_params"] = {"expression": n_attrs["name"]}
                yield shard, node, metadata

    return get_vulnerabilities_from_n_ids_metadata(
        desc_key="lib_root.f052.c_sharp_obsolete_key_derivation",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def get_vuln_instanciation(graph: Graph) -> set[NId]:
    vuln_nodes: set[NId] = set()

    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (
                node.get("label_type") == "ObjectCreation"
                and node.get("name") == "HMACSHA256"
            )
            or (
                node.get("label_type") == "MethodInvocation"
                and node.get("expression") == "HMACSHA256"
            )
        )

    if not library_is_imported(graph, "System.Security.Cryptography"):
        return vuln_nodes

    vuln_nodes.update(g.filter_nodes(graph, graph.nodes, predicate_matcher))
    return vuln_nodes


def eval_danger_case(
    graph: Graph, method: MethodsEnum, dang_case: dict[str, str]
) -> set[NId]:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (
                (node.get("label_type") == "MethodInvocation")
                and (node.get("expression") == dang_case["dang_invocation"])
            )
            or (
                (node.get("label_type") == "ObjectCreation")
                and (node.get("name") == dang_case["dang_invocation"])
            )
        )

    nodes = graph.nodes
    vuln_nodes: set[NId] = set()
    if not library_is_imported(graph, dang_case["dang_lib"]):
        return vuln_nodes
    for n_id in g.filter_nodes(graph, nodes, predicate_matcher):
        if (nodes[n_id].get("label_type") == "MethodInvocation") and (
            nodes[n_id].get("expression") != dang_case["dang_invocation"]
        ):
            continue
        if (args_n_id := g.match_ast_d(graph, n_id, "ArgumentList")) and (
            get_node_evaluation_results(
                method, graph, args_n_id, {"hmacsha256"}, False
            )
        ):
            vuln_nodes.add(n_id)

    return vuln_nodes


def get_vuln_invocations(graph: Graph, method: MethodsEnum) -> set[NId]:
    vuln_nodes: set[NId] = set()
    dang_cases = [
        {
            "dang_lib": "Microsoft.IdentityModel.Tokens",
            "dang_invocation": "SigningCredentials",
        },
        {
            "dang_lib": "Jose",
            "dang_invocation": "JWT.Encode",
        },
    ]
    for dang_case in dang_cases:
        vuln_nodes.update(eval_danger_case(graph, method, dang_case))
    return vuln_nodes


def c_sharp_insec_sign_algorithm(graph_db: GraphDB) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_SIGN_ALGORITHM

    def n_ids() -> Iterator[GraphShardNode]:
        for shard in graph_db.shards_by_language(GraphLanguage.CSHARP):
            if shard.syntax_graph is None:
                continue
            graph = shard.syntax_graph
            for n_id in chain(
                get_vuln_instanciation(graph),
                get_vuln_invocations(graph, method),
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f052.jwt_insecure_signing_algorithm",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
