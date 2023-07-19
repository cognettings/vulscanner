from collections.abc import (
    Iterator,
)
from lib.root.utilities.c_sharp import (
    get_first_member_syntax_graph,
)
from lib.root.utilities.common import (
    check_methods_expression,
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
from symbolic_eval.evaluate import (
    get_node_evaluation_results,
)
from symbolic_eval.utils import (
    get_object_identifiers,
)


def c_sharp_path_injection(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_XPATH_INJECTION
    danger_meths = {"SelectSingleNode"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        xpath_obj = get_object_identifiers(graph, {"XPathNavigator"})

        for node in method_supplies.selected_nodes:
            if check_methods_expression(graph, node, danger_meths) and (
                (memb := get_first_member_syntax_graph(graph, node))
                and graph.nodes[memb].get("symbol") in xpath_obj
                and get_node_evaluation_results(
                    method,
                    graph,
                    node,
                    set(),
                    graph_db=method_supplies.graph_db,
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f021.xpath_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_xpath_injection_evaluate(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_XPATH_INJECTION_EVALUATE
    danger_set = {"userconnection", "userparams"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            if (
                (expr := n_attrs.get("expression"))
                and expr.rsplit(".", maxsplit=1)[-1] == "Evaluate"
                and get_node_evaluation_results(
                    method, graph, n_attrs["expression_id"], {"xpath"}, False
                )
                and (al_id := n_attrs.get("arguments_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    al_id,
                    danger_set,
                    False,
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="f021.xpath_injection_evaluate",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
