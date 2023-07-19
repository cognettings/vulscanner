from collections.abc import (
    Iterable,
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
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_object_identifiers,
)
from utils import (
    graph as g,
)


def is_insecure_decoder(
    method: MethodsEnum,
    graph: Graph,
    n_id: str,
    obj_identifiers: Iterable[str],
    method_supplies: MethodSupplies,
) -> bool:
    exp = graph.nodes[n_id]["expression"]
    memb = graph.nodes[n_id]["member"]
    if (
        exp in obj_identifiers
        and memb == "Decode"
        and (al_id := graph.nodes[g.pred(graph, n_id)[0]].get("arguments_id"))
        and (test_nid := g.match_ast(graph, al_id).get("__2__"))
        and get_node_evaluation_results(
            method, graph, test_nid, set(), graph_db=method_supplies.graph_db
        )
    ):
        return True
    return False


def check_pred(graph: Graph, depth: int = 1, elem_jwt: str = "0") -> bool:
    pred = g.pred(graph, elem_jwt, depth)[0]
    if (
        graph.nodes[pred].get("label_type") == "MemberAccess"
        and graph.nodes[pred].get("member") == "MustVerifySignature"
    ):
        return True
    if graph.nodes[pred].get("label_type") != "VariableDeclaration":
        signed = check_pred(graph, depth + 1, pred)
    else:
        return False
    return signed


def c_sharp_verify_decoder(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_VERIFY_DECODER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        obj_jwt = get_object_identifiers(graph, {"JwtDecoder"})
        for node in method_supplies.selected_nodes:
            if is_insecure_decoder(
                method, graph, node, obj_jwt, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.017.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_jwt_signed_member_access(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_JWT_SIGNED
    object_name = {"JwtBuilder"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get(
                "expression"
            ) in object_name and not check_pred(graph, elem_jwt=node):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.017.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_jwt_signed_object_creation(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_JWT_SIGNED
    object_name = {"JwtBuilder"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("name") in object_name and not check_pred(
                graph, elem_jwt=node
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="criteria.vulns.017.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
