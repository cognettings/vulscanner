from collections.abc import (
    Iterator,
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
from utils.graph import (
    adj_ast,
    pred_ast,
)


def python_regex_dos(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.PYTHON_REGEX_DOS
    danger_set = {"re.match", "re.findall", "re.search"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            n_attrs = graph.nodes[n_id]
            expr = f'{n_attrs["expression"]}.{n_attrs["member"]}'
            parent_id = pred_ast(graph, n_id)[0]
            if (
                expr in danger_set
                and (al_id := graph.nodes[parent_id].get("arguments_id"))
                and (args_ids := adj_ast(graph, al_id))
                and len(args_ids) >= 2
                and get_node_evaluation_results(
                    method, graph, args_ids[0], {"userparams"}
                )
            ):
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f211.regex_vulnerable",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
