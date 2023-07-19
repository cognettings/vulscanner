from collections.abc import (
    Iterable,
)
from itertools import (
    chain,
)
from lib.root.utilities.javascript import (
    get_default_alias,
    get_named_alias,
    get_namespace_alias,
)
from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    MethodSupplies,
    NId,
)
from symbolic_eval.evaluate import (
    evaluate,
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)

CS_INSECURE_CIPHERS = {
    "AesFastEngine",
    "DES",
    "DESCryptoServiceProvider",
    "DesEdeEngine",
    "DSACryptoServiceProvider",
    "RC2",
    "RC2CryptoServiceProvider",
    "RijndaelManaged",
    "TripleDES",
    "TripleDESCng",
    "TripleDESCryptoServiceProvider",
    "Blowfish",
}

CS_INSECURE_HASH = {
    "HMACMD5",
    "HMACRIPEMD160",
    "HMACSHA1",
    "MACTripleDES",
    "MD5",
    "MD5Cng",
    "MD5CryptoServiceProvider",
    "MD5Managed",
    "RIPEMD160",
    "RIPEMD160Managed",
    "SHA1",
    "SHA1Cng",
    "SHA1CryptoServiceProvider",
    "SHA1Managed",
}


def split_function_name(f_names: str) -> tuple[str, str]:
    name_l = f_names.lower().split(".")
    if len(name_l) < 2:
        return "", name_l[-1]
    return name_l[-2], name_l[-1]


def is_insecure_encrypt(
    graph: Graph, al_id: NId, algo: str, method: MethodsEnum
) -> bool:
    if algo in {"des", "rc4"}:
        return True
    if (
        algo in {"aes", "rsa"}
        and (args := g.adj_ast(graph, al_id))
        and len(args) > 2
    ):
        return get_node_evaluation_results(method, graph, args[-1], set())
    return False


def insecure_create_cipher(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> list[NId]:
    vuln_nodes: list[NId] = []
    ciphers_methods = {
        "createdecipher",
        "createcipher",
        "createdecipheriv",
        "createcipheriv",
    }
    for n_id in method_supplies.selected_nodes:
        f_name = graph.nodes[n_id]["expression"]
        _, crypt = split_function_name(f_name)
        if (
            crypt in ciphers_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 0
            and get_node_evaluation_results(method, graph, args[0], set())
        ):
            vuln_nodes.append(n_id)

    return vuln_nodes


def insecure_hash(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_methods = complete_attrs_on_set({"crypto.createHash"})

    for n_id in method_supplies.selected_nodes:
        if (
            graph.nodes[n_id]["expression"] in danger_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (test_node := g.match_ast(graph, al_id).get("__0__"))
            and get_node_evaluation_results(method, graph, test_node, set())
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_encrypt(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> list[NId]:
    vuln_nodes: list[NId] = []
    crypto_methods = {"encrypt", "decrypt"}

    for n_id in method_supplies.selected_nodes:
        f_name = graph.nodes[n_id]["expression"]
        algo, crypt = split_function_name(f_name)
        if (
            crypt in crypto_methods
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and is_insecure_encrypt(graph, al_id, algo, method)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_ecdh_key(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_f = {"createecdh"}

    for n_id in method_supplies.selected_nodes:
        f_name = graph.nodes[n_id]["expression"]
        _, key = split_function_name(f_name)
        if (
            key in danger_f
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 0
            and get_node_evaluation_results(method, graph, args[0], set())
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_rsa_keypair(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_f = {"generatekeypair"}
    rules = {"rsa", "unsafemodulus"}

    for n_id in method_supplies.selected_nodes:
        f_name = graph.nodes[n_id]["expression"]
        _, key = split_function_name(f_name)
        if (
            key in danger_f
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 1
            and get_node_evaluation_results(method, graph, al_id, rules)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_ec_keypair(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> list[NId]:
    vuln_nodes: list[NId] = []
    danger_f = {"generatekeypair"}
    rules = {"ec", "unsafecurve"}

    for n_id in method_supplies.selected_nodes:
        f_name = graph.nodes[n_id]["expression"]
        _, key = split_function_name(f_name)
        if (
            key in danger_f
            and (al_id := graph.nodes[n_id].get("arguments_id"))
            and (args := g.adj_ast(graph, al_id))
            and len(args) > 1
            and get_node_evaluation_results(method, graph, al_id, rules)
        ):
            vuln_nodes.append(n_id)
    return vuln_nodes


def insecure_hash_library(
    graph: Graph,
    method_supplies: MethodSupplies,
) -> list[NId]:
    vuln_nodes: list[NId] = []
    if dangerous_name := get_default_alias(graph, "js-sha1"):
        for n_id in method_supplies.selected_nodes:
            method_expression = graph.nodes[n_id]["expression"]
            if method_expression.split(".")[0] == dangerous_name:
                vuln_nodes.append(n_id)
    return vuln_nodes


def get_danger_n_id(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> NId | None:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation:
            if evaluation.danger:
                return n_id
            if vuln_n_id := next(iter(evaluation.triggers), None):
                return vuln_n_id
    return None


def jwt_insecure_sign(
    graph: Graph, method: MethodsEnum, method_supplies: MethodSupplies
) -> list[NId]:
    nodes = graph.nodes
    vuln_nodes: list[NId] = []
    if imported_name := get_default_alias(graph, "jsonwebtoken"):
        for n_id in method_supplies.selected_nodes:
            expression = graph.nodes[n_id]["expression"]
            if expression == f"{imported_name}.sign":
                method_args_n_ids = g.adj_ast(
                    graph, nodes[n_id].get("arguments_id"), 1
                )
                if len(method_args_n_ids) < 3 or nodes[
                    method_args_n_ids[2]
                ].get("label_type") not in {"Object", "SymbolLookup"}:
                    vuln_nodes.append(n_id)
                    continue

                if vuln_node := get_danger_n_id(
                    graph, method_args_n_ids[2], method
                ):
                    vuln_nodes.append(vuln_node)
    return vuln_nodes


def jwt_insec_sign_async(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> list[NId]:
    def match_predicate(node: dict[str, str]) -> bool:
        return bool(
            (n_exp := node.get("expression"))
            and (
                (n_exp.startswith(f"new{imported_name}"))
                or (n_exp.endswith("setProtectedHeader"))
            )
        )

    nodes = graph.nodes
    vuln_nodes: list[NId] = []
    imported_name = get_default_alias(graph, "jose") or get_namespace_alias(
        graph, "jose"
    )

    for n_id in g.filter_nodes(
        graph, method_supplies.selected_nodes, match_predicate
    ):
        if (
            (args_n_id := nodes[n_id].get("arguments_id"))
            and (susp_n_id := next(iter(g.adj_ast(graph, args_n_id)), None))
            and get_node_evaluation_results(method, graph, susp_n_id, set())
        ):
            vuln_nodes.append(susp_n_id)
    return vuln_nodes


def get_insec_auth_default_import(
    graph: Graph, method_supplies: MethodSupplies
) -> tuple[NId, ...]:
    def match_predicate(node: dict[str, str]) -> bool:
        if imported_name:
            danger_methods = {
                f"{imported_name}.HmacSHA1",
                f"{imported_name}.HmacSHA256",
            }
            return node.get("expression") in danger_methods
        return False

    imported_name = get_default_alias(
        graph, "crypto-js"
    ) or get_namespace_alias(graph, "crypto-js")

    return g.filter_nodes(
        graph, method_supplies.selected_nodes, match_predicate
    )


def get_insec_auth_direct_import(
    graph: Graph, method_supplies: MethodSupplies
) -> tuple[NId, ...]:
    def match_predicate(node: dict[str, str]) -> bool:
        if dang_names != {None}:
            return node.get("expression") in dang_names
        return False

    dang_names = {
        get_default_alias(graph, "crypto-js/hmac-sha1"),
        get_default_alias(graph, "crypto-js/hmac-sha256"),
    }

    return g.filter_nodes(
        graph, method_supplies.selected_nodes, match_predicate
    )


def get_first_arg_eval(
    graph: Graph, n_id: NId, method: MethodsEnum
) -> NId | None:
    if (
        (args_n_id := graph.nodes[n_id].get("arguments_id"))
        and (first_arg_n_id := next(iter(g.adj_ast(graph, args_n_id)), None))
        and get_node_evaluation_results(method, graph, first_arg_n_id, set())
    ):
        return first_arg_n_id
    return None


def get_insec_auth_crypto_lib_named(
    graph: Graph, method: MethodsEnum, method_supplies: MethodSupplies
) -> list[NId]:
    vuln_nodes: list[NId] = []

    if imported_name := get_named_alias(graph, "crypto", "createHmac"):
        for n_id in method_supplies.selected_nodes:
            if graph.nodes[n_id]["expression"] == imported_name and (
                vuln_n_id := get_first_arg_eval(graph, n_id, method)
            ):
                vuln_nodes.append(vuln_n_id)
    return vuln_nodes


def get_insec_auth_crypto_lib(
    graph: Graph, method: MethodsEnum, method_supplies: MethodSupplies
) -> list[NId]:
    def match_predicate(node: dict[str, str]) -> bool:
        return bool(
            (imported_name)
            and (node.get("expression") == f"{imported_name}.createHmac")
        )

    vuln_nodes: list[NId] = []
    nodes = method_supplies.selected_nodes
    imported_name = get_default_alias(graph, "crypto") or get_namespace_alias(
        graph, "crypto"
    )

    for n_id in g.filter_nodes(graph, nodes, match_predicate):
        if vuln_n_id := get_first_arg_eval(graph, n_id, method):
            vuln_nodes.append(vuln_n_id)
    return vuln_nodes


def insec_msg_auth_mechanism(
    graph: Graph,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> Iterable[NId]:
    return chain(
        get_insec_auth_default_import(graph, method_supplies),
        get_insec_auth_direct_import(graph, method_supplies),
        get_insec_auth_crypto_lib(graph, method, method_supplies),
        get_insec_auth_crypto_lib_named(graph, method, method_supplies),
    )
