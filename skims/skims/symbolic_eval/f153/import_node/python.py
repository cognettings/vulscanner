from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
)

REQUESTS_LIBRARIES = {
    "requests",
    "urllib",
    "urllib2",
    "urllib3",
    "httplib2",
    "httplib",
    "http",
    "treq",
    "aiohttp",
}


def is_library_for_requests(graph: Graph, c_id: NId) -> bool:
    if graph.nodes[c_id].get("module") in REQUESTS_LIBRARIES:
        return True
    return False


def danger_mime_type(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    is_request_library = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs.get("import_type") == "multiple_import":
        for c_id in adj_ast(args.graph, args.n_id):
            if is_library_for_requests(args.graph, c_id):
                is_request_library = True
    elif is_library_for_requests(args.graph, args.n_id):
        is_request_library = True

    if is_request_library:
        args.triggers.add("client_connection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
