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
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)


def is_logger_unsafe(
    method: MethodsEnum,
    graph: Graph,
    n_id: str,
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            (
                evaluation := evaluate(
                    method, graph, path, n_id, method_supplies.graph_db
                )
            )
            and evaluation.danger
            and {"userparams", "userconnection"}.issubset(evaluation.triggers)
            and not {"sanitize", "allchars"}.issubset(evaluation.triggers)
        ):
            return True
    return False


def java_insecure_logging(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_INSECURE_LOGGING

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            n_attrs = graph.nodes[node]
            if (
                n_attrs["expression"] in {"info", "debug"}
                and (obj_id := n_attrs.get("object_id"))
                and graph.nodes[obj_id].get("symbol") in {"log", "Logger"}
                and (al_id := graph.nodes[node].get("arguments_id"))
                and is_logger_unsafe(method, graph, al_id, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f091.log_injection",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
