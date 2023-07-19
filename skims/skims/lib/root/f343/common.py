from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def is_vuln(graph: Graph, method: MethodsEnum, n_id: NId) -> NId | None:
    for path in get_backward_paths(graph, n_id):
        if evaluation := evaluate(method, graph, path, n_id):
            if "custom_function" in evaluation.triggers:
                return None
            if "algorithm" not in evaluation.triggers:
                return n_id
            if "gzip" in evaluation.triggers:
                evaluation.triggers.difference_update({"algorithm", "gzip"})
                alg_n_id = next(iter(evaluation.triggers))
                return alg_n_id
    return None


def webpack_insecure_compression(
    graph: Graph, danger_library: str, n_id: NId, method: MethodsEnum
) -> NId | None:
    if (
        graph.nodes[n_id].get("name") == danger_library
        and (parameters_n_id := g.match_ast_d(graph, n_id, "ArgumentList"))
        and (vuln_n_id := is_vuln(graph, method, parameters_n_id))
    ):
        return vuln_n_id
    return None
