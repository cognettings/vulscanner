from collections.abc import (
    Iterator,
)
from lib.root.utilities.common import (
    check_methods_expression,
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


def get_triggers_eval(
    method: MethodsEnum,
    graph: Graph,
    n_id: NId,
    danger_set: set[str],
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(
            method, graph, path, n_id, graph_db=method_supplies.graph_db
        )
        if evaluation and evaluation.triggers == danger_set:
            return True
    return False


def c_sharp_unsafe_addheader_write(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_ADDHEADER_WRITE
    danger_methods = {"AddHeader", "Write"}
    danger_set = {"userconnection", "userparams"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if check_methods_expression(
                graph, node, danger_methods
            ) and get_node_evaluation_results(
                method,
                graph,
                node,
                danger_set,
                graph_db=method_supplies.graph_db,
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f008.insec_addheader_write",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_unsafe_status_write(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_INSEC_ADDHEADER_WRITE
    danger_set = {"userconnection", "userparams"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            parent_id = g.pred_ast(graph, node)[0]
            if (
                n_attrs["member"] == "StatusDescription"
                and (val_id := graph.nodes[parent_id].get("value_id"))
                and get_node_evaluation_results(
                    method,
                    graph,
                    n_attrs["expression_id"],
                    set(),
                    graph_db=method_supplies.graph_db,
                )
                and get_triggers_eval(
                    method, graph, val_id, danger_set, method_supplies
                )
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f008.insec_addheader_write",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
