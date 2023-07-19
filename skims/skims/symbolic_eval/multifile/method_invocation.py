from model.graph import (
    Graph,
    GraphShardMetadataLanguage,
    NId,
)
from symbolic_eval.types import (
    SymbolicEvalArgs,
)
from symbolic_eval.utils import (
    get_backward_paths,
    get_current_class,
)
from utils import (
    graph as g,
)


def get_return_nodes(graph: Graph, range_nids: list) -> list[NId]:
    return_nodes = g.filter_nodes(
        graph, graph.nodes, g.pred_has_labels(label_type="Return")
    )
    return list(set(range_nids) & set(return_nodes))


def evaluate_file(
    args: SymbolicEvalArgs, obj_construct: str, file: str, struct: dict
) -> bool:
    danger = False
    n_attrs = args.graph.nodes[args.n_id]
    if args.graph_db and obj_construct in struct:
        class_data = struct[obj_construct]["data"]
        node_range = class_data[n_attrs["expression"]].get("node_range")
        graph = (
            shard.syntax_graph
            if (shard := args.graph_db.shards_by_path_f(file))
            else None
        )
        if graph:
            return_nodes = get_return_nodes(graph=graph, range_nids=node_range)
            for node in return_nodes:
                danger = any(
                    args.generic(args.fork_n_id(node, path, graph))
                    for path in get_backward_paths(graph, node)
                )
    return danger


def evaluate_method_invocation(
    args: SymbolicEvalArgs, lang: GraphShardMetadataLanguage
) -> bool:
    n_attrs = args.graph.nodes[args.n_id]

    metadata_node = args.graph.nodes["0"]
    current_class = args.graph.nodes[get_current_class(args.graph, args.n_id)][
        "name"
    ]

    if (
        (obj_id := n_attrs.get("object_id"))
        and (object_method := args.graph.nodes[obj_id].get("symbol"))
        and (class_instances := metadata_node["instances"].get(current_class))
        and args.graph_db
    ):
        lang_context = args.graph_db.context[lang]
        obj_instance = class_instances.get(object_method)
        package_context = lang_context.get(obj_instance["package"])
        if lang_context and obj_instance and package_context:
            for file, struct in package_context.items():
                return evaluate_file(
                    args, obj_instance["object"], file, struct
                )
    return False
