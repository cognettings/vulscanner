from collections.abc import (
    Iterator,
)
from lib.root.utilities.c_sharp import (
    get_first_member_syntax_graph,
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
from utils import (
    graph as g,
)


def get_insecure_vars(graph: Graph) -> list[str]:
    object_names = {"CorsPolicyBuilder"}
    insecure_vars = []
    for nid in g.matching_nodes(graph, label_type="ObjectCreation"):
        if (
            graph.nodes[nid].get("label_type") == "ObjectCreation"
            and graph.nodes[nid].get("name") in object_names
        ):
            var_nid = g.pred_ast(graph, nid)[0]
            if graph.nodes[var_nid].get("label_type") == "VariableDeclaration":
                insecure_vars.append(graph.nodes[var_nid].get("variable"))
    return insecure_vars


def is_insecure_use_cors(graph: Graph, nid: NId) -> bool:
    al_id = graph.nodes[g.pred(graph, nid)[0]].get("arguments_id")
    arg_nid = g.match_ast(graph, al_id).get("__0__")
    if not arg_nid:
        return False

    n_attrs = graph.nodes[arg_nid]
    if (
        n_attrs["label_type"] == "MemberAccess"
        and n_attrs.get("member") == "AllowAll"
    ) or (
        n_attrs["label_type"] == "MethodDeclaration"
        and (m_id := n_attrs["block_id"])
        and "AllowAnyOrigin" in graph.nodes[m_id].get("expression").split(".")
    ):
        return True

    return False


def is_vulnerable_enable_attribute(
    method: MethodsEnum,
    graph: Graph,
    n_id: NId,
    name: str,
    method_supplies: MethodSupplies,
) -> bool:
    if name.lower() != "enablecors" or not (
        al_id := g.match_ast_d(graph, n_id, "ArgumentList")
    ):
        return False

    for arg in g.adj_ast(graph, al_id):
        n_attrs = graph.nodes[arg]
        if (
            n_attrs["label_type"] == "NamedArgument"
            and n_attrs["argument_name"].lower() == "origins"
            and get_node_evaluation_results(
                method,
                graph,
                n_attrs["value_id"],
                set(),
                graph_db=method_supplies.graph_db,
            )
        ):
            return True

    return False


def is_vulnerable_policy(graph: Graph, n_id: NId) -> bool:
    if (
        (al_id := graph.nodes[n_id].get("arguments_id"))
        and (al_list := g.adj_ast(graph, al_id))
        and len(al_list) >= 2
        and graph.nodes[al_list[1]]["label_type"] == "MethodDeclaration"
    ):
        block_id = graph.nodes[al_list[1]]["block_id"]
        if graph.nodes[block_id]["label_type"] == "ExecutionBlock":
            m_id = g.match_ast(graph, block_id).get("__0__")
        else:
            m_id = block_id

        expr = graph.nodes[m_id].get("expression")
        if "AllowAnyOrigin" in expr:
            return True

    return False


def is_vulnerable_origin(
    graph: Graph, nid: NId, expr: str, method_supplies: MethodSupplies
) -> bool:
    method = MethodsEnum.CS_INSECURE_CORS_ORIGIN
    if "addpolicy" in expr.lower() and is_vulnerable_policy(graph, nid):
        return True

    if (
        "origins.add" in expr.lower()
        and (fr_m := get_first_member_syntax_graph(graph, nid))
        and get_node_evaluation_results(method, graph, fr_m, {"CorsObject"})
        and (arg_id := graph.nodes[nid].get("arguments_id"))
    ):
        childs = g.adj_ast(graph, arg_id)
        if len(childs) > 0 and get_node_evaluation_results(
            method, graph, childs[0], set(), graph_db=method_supplies.graph_db
        ):
            return True

    return False


def c_sharp_insecure_cors(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_CORS

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        insecure_vars = get_insecure_vars(graph)
        for node in method_supplies.selected_nodes:
            if (
                graph.nodes[node].get("member") == "AllowAnyOrigin"
                and graph.nodes[node].get("expression").split(".")[0]
                in insecure_vars
            ) or (
                graph.nodes[node].get("member") == "UseCors"
                and is_insecure_use_cors(graph, node)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_insecure_cors_origin_method(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_CORS_ORIGIN

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for node in method_supplies.selected_nodes:
            expr = graph.nodes[node].get("expression")
            if is_vulnerable_origin(graph, node, expr, method_supplies):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_insecure_cors_origin_attribute(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSECURE_CORS_ORIGIN

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph

        for node in method_supplies.selected_nodes:
            name = graph.nodes[node].get("name")
            if is_vulnerable_enable_attribute(
                method, graph, node, name, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f134.cors_policy_allows_any_origin",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
