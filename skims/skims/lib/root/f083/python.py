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
    get_node_evaluation_results,
)
from utils import (
    graph as g,
)


def get_eval_danger(
    graph: Graph, n_ids: list[NId], method: MethodsEnum
) -> bool:
    for _id in n_ids:
        if graph.nodes[_id]["argument_name"] != "resolve_entities":
            continue
        val_id = graph.nodes[_id]["value_id"]
        return get_node_evaluation_results(method, graph, val_id, set())
    return False


def is_xml_parser_vuln(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    al_id = g.match_ast_d(graph, n_id, "ArgumentList")
    if al_id and (
        not (args := g.match_ast_group_d(graph, al_id, "NamedArgument"))
        or get_eval_danger(graph, args, method)
    ):
        return True
    return False


def python_xml_parser(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_XML_PARSER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if graph.nodes[n_id][
                "expression"
            ] == "etree.XMLParser" and is_xml_parser_vuln(graph, n_id, method):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f083.generic_xml_parser",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
