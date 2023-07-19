from symbolic_eval.common import (
    PYTHON_REQUESTS_LIBRARIES,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
from utils.graph import (
    adj_ast,
)


def python_danger_auth(args: SymbolicEvalArgs) -> SymbolicEvaluation:
    is_request_library = False
    n_attrs = args.graph.nodes[args.n_id]
    if n_attrs.get("import_type") == "multiple_import":
        for c_id in adj_ast(args.graph, args.n_id):
            if (
                args.graph.nodes[c_id].get("module")
                in PYTHON_REQUESTS_LIBRARIES
            ):
                is_request_library = True
    elif n_attrs.get("module") in PYTHON_REQUESTS_LIBRARIES:
        is_request_library = True

    if is_request_library:
        args.triggers.add("client_connection")

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
