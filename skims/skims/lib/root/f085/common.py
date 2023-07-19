from model.core import (
    MethodsEnum,
)
from model.graph import (
    Graph,
    NId,
)
import re
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)


def could_be_boolean(key: str) -> bool:
    prefixes = {"is", "has", "es"}
    match = re.search("[a-z]", key, re.I)
    if match:
        _key = key[match.start() :]
        return any(_key.startswith(prefix) for prefix in prefixes)
    return False


def is_smell_dangerous(values: set[str]) -> bool:
    conditions = {
        "auth",
        "credential",
        "documentousuario",
        "jwt",
        "password",
        "sesiondata",
        "sesionid",
        "sesiontoken",
        "sessiondata",
        "sessionid",
        "sessiontoken",
        "tokenaccess",
        "tokenapp",
        "tokenid",
        "nameuser",
        "nombreusuario",
        "mailuser",
    }

    item = re.sub("[^A-Za-z0-9]+", "", "".join(values)).lower()
    if item in conditions and not could_be_boolean(item):
        return True
    return False


def is_insecure_storage(graph: Graph, nid: NId, method: MethodsEnum) -> bool:
    f_name = graph.nodes[nid]["expression"]
    al_id = graph.nodes[nid].get("arguments_id")
    if not al_id:
        return False
    opc_nid = g.match_ast(graph, al_id)

    if "getItem" in f_name.split("."):
        test_node = opc_nid.get("__0__")
    else:
        test_node = opc_nid.get("__1__")

    if not test_node:
        return False

    for path in get_backward_paths(graph, test_node):
        if (
            evaluation := evaluate(method, graph, path, test_node)
        ) and is_smell_dangerous(evaluation.triggers):
            return True
    return False


def client_storage(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    danger_names = {
        "localStorage.getItem",
        "localStorage.setItem",
        "sessionStorage.getItem",
        "sessionStorage.setItem",
    }
    f_name = graph.nodes[n_id].get("expression")
    if f_name in danger_names and is_insecure_storage(graph, n_id, method):
        return True
    return False
