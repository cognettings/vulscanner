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


def get_regex_node(graph: Graph, expr: str) -> NId | None:
    if regex_name := expr.split(".")[0]:
        for vid in g.matching_nodes(graph, label_type="VariableDeclaration"):
            if graph.nodes[vid].get("variable") == regex_name:
                return vid
    return None


def sets_timespan(method: MethodsEnum, graph: Graph, n_id: NId) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if evaluation and "hastimespan" in evaluation.triggers:
            return True
    return False


def is_pattern_danger(method: MethodsEnum, graph: Graph, n_id: NId) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and "safepattern" not in evaluation.triggers
        ):
            return True
    return False


def is_regex_vuln(method: MethodsEnum, graph: Graph, n_id: NId) -> bool:
    obj_c = g.match_ast(graph, n_id, "ObjectCreation").get("ObjectCreation")
    if (
        obj_c
        and graph.nodes[obj_c].get("name") == "Regex"
        and (al_id := g.get_ast_childs(graph, obj_c, "ArgumentList")[0])
    ):
        args_nids = g.adj_ast(graph, al_id)
        regpat_nid = args_nids[0]
        is_danger_pattern = is_pattern_danger(method, graph, regpat_nid)
        has_timespan = False
        if len(args_nids) == 3:
            timespan_nid = args_nids[2]
            has_timespan = sets_timespan(method, graph, timespan_nid)

        return is_danger_pattern and not has_timespan

    return False


def analyze_method_vuln(
    method: MethodsEnum, graph: Graph, method_id: NId
) -> bool:
    method_n = graph.nodes[method_id]
    expr = method_n.get("expression")
    args_id = g.get_ast_childs(graph, method_id, "ArgumentList")
    args_nids = g.adj_ast(graph, args_id[0])

    if len(args_nids) == 0 or not get_node_evaluation_results(
        method, graph, args_nids[0], {"userparams", "userconnection"}, False
    ):
        return False

    if len(args_nids) == 1:
        is_danger_method = True
    elif len(args_nids) >= 2:
        regpat_nid = args_nids[1]
        is_danger_method = is_pattern_danger(method, graph, regpat_nid)

    if len(args_nids) == 4:
        timespan_nid = args_nids[3]
        is_danger_method = not sets_timespan(method, graph, timespan_nid)

    if (
        is_danger_method
        and (regex_node := get_regex_node(graph, expr))
        and is_regex_vuln(method, graph, regex_node)
    ):
        return True

    return False


def c_sharp_vuln_regular_expression(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_VULN_REGEX
    regex_methods = {"IsMatch", "Match", "Matches"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            method_id = g.pred_ast(graph, node)[0]
            if graph.nodes[node].get(
                "member"
            ) in regex_methods and analyze_method_vuln(
                method, graph, method_id
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_regex_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_REGEX_INJETCION
    danger_methods = {"Regex"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            pred = g.pred_ast(graph, node)[0]
            if (
                graph.nodes[node].get("expression") in danger_methods
                and graph.nodes[node]["member"] == "Match"
                and get_node_evaluation_results(
                    method,
                    graph,
                    pred,
                    set(),
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, pred

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
