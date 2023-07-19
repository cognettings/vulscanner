from lib.root.f052.common import (
    split_function_name,
)
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


def is_logger_unsafe(graph: Graph, n_id: str, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers != {"sanitized", "characters"}
        ):
            return True

    return False


def insecure_logging(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    danger_objects = {
        "console",
        "logger",
        "log",
    }
    danger_methods = {
        "info",
        "warn",
        "error",
        "trace",
        "debug",
    }
    f_name = graph.nodes[n_id]["expression"]
    obj, funct = split_function_name(f_name)
    if (
        obj in danger_objects
        and funct in danger_methods
        and (test_nid := graph.nodes[n_id].get("arguments_id"))
        and is_logger_unsafe(graph, test_nid, method)
    ):
        return True
    return False
