from model.graph import (
    Graph,
    NId,
)
import re
from symbolic_eval.common import (
    INSECURE_HASHES,
)
from symbolic_eval.multifile.utils.load_from_properties import (
    parse_properties,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
    SymbolicEvaluation,
)
import utils.graph as g


def get_first_string(graph: Graph, n_id: NId) -> str | None:
    if first_str := g.match_ast_d(graph, n_id, "Literal", -1):
        return graph.nodes[first_str].get("value")
    return None


def get_file_names(args: SymbolicEvalArgs) -> set[str]:
    graph = args.graph
    var_name_matcher = re.compile(r"loader_name__.+")
    loader_vars_raw = filter(var_name_matcher.match, args.triggers)
    loader_vars = [*map(lambda x: x.split("__")[1], loader_vars_raw)]

    loader_nodes: set[NId] = set()

    for n_id in g.matching_nodes(
        graph, label_type="MethodInvocation", expression="load"
    ):
        if (obj_id := graph.nodes[n_id].get("object_id")) and (
            graph.nodes[obj_id].get("symbol") in loader_vars
        ):
            loader_nodes.add(n_id)

    loader_file_names: set[str] = set()
    for loader_node in loader_nodes:
        if (file_name := get_first_string(graph, loader_node)) and (
            ".properties" in file_name
        ):
            loader_file_names.add(file_name[1:-1])
    return loader_file_names


def java_insecure_hash(
    args: SymbolicEvalArgs,
) -> SymbolicEvaluation:
    graph = args.graph
    nodes = graph.nodes
    node = nodes[args.n_id]

    if "0" not in nodes:
        return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)

    if (node.get("variable_type") == "java.util.Properties") and (
        var_name := node.get("variable")
    ):
        args.triggers.add(f"loader_name__{var_name}")

    if (
        (val_id := node.get("value_id"))
        and (nodes[val_id].get("expression") == "getProperty")
        and (args_id := nodes[val_id].get("arguments_id"))
        and (load_key := get_first_string(graph, args_id))
        and (file_names := get_file_names(args))
    ):
        property_value = parse_properties(file_names, load_key)
        if property_value in INSECURE_HASHES:
            args.evaluation[args.n_id] = True

    return SymbolicEvaluation(args.evaluation[args.n_id], args.triggers)
