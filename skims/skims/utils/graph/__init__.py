from collections.abc import (
    Iterable,
    Iterator,
)
from itertools import (
    chain,
)
from model.graph import (
    Graph,
    NAttrs,
    NAttrsPredicateFunction,
    NId,
    NIdPredicateFunction,
)
import networkx as nx
import os
from typing import (
    Any,
)
from utils.logs import (
    log_blocking,
)
from utils.system import (
    read_blocking,
)

CFG = dict(label_cfg="CFG")
GRAPH_STYLE_ATTRS = {"arrowhead", "color", "fillcolor", "label", "style"}
ROOT_NODE: str = "1"


def to_svg(graph: Graph, path: str) -> bool:
    nx.drawing.nx_agraph.write_dot(graph, path)

    code, _, stderr = read_blocking("dot", "-O", "-T", "svg", path)

    if code == 0:
        os.unlink(path)
        return True

    log_blocking("debug", "Error while generating svg: %s", stderr.decode())
    return False


def has_labels(n_attrs: NAttrs, **expected_attrs: str) -> bool:
    return all(
        n_attrs.get(expected_attr) == expected_attr_value
        for expected_attr, expected_attr_value in expected_attrs.items()
    )


def pred_has_labels(**expected_attrs: str) -> NAttrsPredicateFunction:
    def predicate(n_attrs: NAttrs) -> bool:
        return has_labels(n_attrs, **expected_attrs)

    return predicate


def filter_nodes(
    graph: Graph,
    nodes: Iterable[NId],
    predicate: NAttrsPredicateFunction,
) -> tuple[NId, ...]:
    result: tuple[NId, ...] = tuple(
        n_id for n_id in nodes if predicate(graph.nodes[n_id])
    )

    return result


def matching_nodes(graph: Graph, **expected_attrs: str) -> tuple[NId, ...]:
    return filter_nodes(graph, graph.nodes, pred_has_labels(**expected_attrs))


def _append_direct_childs(
    graph: Graph,
    childs: list[NId],
    n_id: NId,
    strict: bool,
    edge_keys: set[str],
    **edge_attrs: str,
) -> Iterator[NId]:
    # Append direct childs
    for c_id in childs:
        process = has_labels(graph[n_id][c_id], **edge_attrs)
        if strict and process:
            graph_edge_keys = set(graph[n_id][c_id].keys())
            difference = graph_edge_keys.difference(edge_keys)
            process = not bool(difference) or difference == {"label_index"}
        if process:
            yield c_id


def adj_lazy(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    strict: bool = False,
    _processed_n_ids: set[NId] | None = None,
    **edge_attrs: str,
) -> Iterator[NId]:
    """Return adjacent nodes to `n_id`, following just edges with given attrs.

    - Parameter `depth` may be -1 to indicate infinite depth.
    - Parameter `strict` indicates that the edges must have only the indicated
      attributes

    - Search is done breadth first.
    - Nodes are returned ordered ascending by index on each level.

    This function must be used instead of graph.adj, because graph.adj
    becomes unstable (unordered) after mutating the graph, also this allow
    following just edges matching `edge_attrs`.
    """
    processed_n_ids: set[str] = _processed_n_ids or set()
    if depth == 0 or n_id in processed_n_ids:
        return

    processed_n_ids.add(n_id)

    childs: list[str] = sorted(graph.adj[n_id], key=int)

    edge_keys = set(edge_attrs.keys())

    # Append direct childs
    yield from _append_direct_childs(
        graph, childs, n_id, strict, edge_keys, **edge_attrs
    )

    # Recurse into childs
    if depth < 0 or depth > 1:
        for c_id in childs:
            process = has_labels(graph[n_id][c_id], **edge_attrs)
            if process and strict:
                graph_edge_keys = set(graph[n_id][c_id].keys())
                difference = graph_edge_keys.difference(edge_keys)
                process = not bool(difference) or difference == {"label_index"}
            if process:
                yield from adj_lazy(
                    graph,
                    c_id,
                    depth=depth - 1,
                    strict=strict,
                    _processed_n_ids=processed_n_ids,
                    **edge_attrs,
                )


def adj(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    strict: bool = False,
    _processed_n_ids: set[NId] | None = None,
    **edge_attrs: str,
) -> tuple[NId, ...]:
    return tuple(
        adj_lazy(
            graph,
            n_id,
            depth=depth,
            strict=strict,
            _processed_n_ids=_processed_n_ids,
            **edge_attrs,
        )
    )


def adj_ast(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> tuple[NId, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, strict=strict, label_ast="AST")
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def adj_ctx(
    graph: Graph,
    n_id: str,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> tuple[NId, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, strict=strict, label_ctx="CTX")
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def adj_cfg(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> tuple[NId, ...]:
    return tuple(
        c_id
        for c_id in adj(graph, n_id, depth, strict=strict, label_cfg="CFG")
        if has_labels(graph.nodes[c_id], **n_attrs)
    )


def adj_cfg_lazy(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    strict: bool = False,
    **n_attrs: str,
) -> Iterator[str]:
    yield from adj_lazy(
        graph,
        n_id,
        depth=depth,
        strict=strict,
        _processed_n_ids=set(),
        label_cfg="CFG",
        **n_attrs,
    )


def pred_lazy(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    _processed_n_ids: set[str] | None = None,
    **edge_attrs: str,
) -> Iterator[NId]:
    """Same as `adj` but follow edges in the opposite direction."""
    processed_n_ids: set[NId] = _processed_n_ids or set()
    if depth == 0 or n_id in processed_n_ids:
        return

    processed_n_ids.add(n_id)

    p_ids: list[str] = sorted(graph.pred[n_id], key=int)

    # Append direct parents
    for p_id in p_ids:
        if has_labels(graph[p_id][n_id], **edge_attrs):
            yield p_id

    # Recurse into parents
    if depth < 0 or depth > 1:
        for p_id in p_ids:
            if has_labels(graph[p_id][n_id], **edge_attrs):
                yield from pred_lazy(
                    graph,
                    p_id,
                    depth=depth - 1,
                    _processed_n_ids=processed_n_ids,
                    **edge_attrs,
                )


def pred(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    _processed_n_ids: set[NId] | None = None,
    **edge_attrs: str,
) -> tuple[NId, ...]:
    return tuple(
        pred_lazy(
            graph,
            n_id,
            depth,
            _processed_n_ids=_processed_n_ids,
            **edge_attrs,
        )
    )


def pred_ast(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    **edge_attrs: str,
) -> tuple[NId, ...]:
    return tuple(pred_ast_lazy(graph, n_id, depth, **edge_attrs))


def pred_ast_lazy(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    **edge_attrs: str,
) -> Iterator[NId]:
    yield from pred_lazy(
        graph,
        n_id,
        depth,
        _processed_n_ids=set(),
        label_ast="AST",
        **edge_attrs,
    )


def pred_cfg(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    **edge_attrs: str,
) -> tuple[NId, ...]:
    return tuple(pred_cfg_lazy(graph, n_id, depth, **edge_attrs))


def pred_cfg_lazy(
    graph: Graph,
    n_id: NId,
    depth: int = 1,
    **edge_attrs: str,
) -> Iterator[NId]:
    yield from pred_lazy(
        graph,
        n_id,
        depth,
        _processed_n_ids=set(),
        label_cfg="CFG",
        **edge_attrs,
    )


def match_ast(
    graph: Graph,
    n_id: NId,
    *label_type: str,
    depth: int = 1,
) -> dict[str, NId | None]:
    index: int = 0
    nodes: dict[str, NId | None] = dict.fromkeys(label_type)

    for c_id in adj_ast(graph, n_id, depth=depth):
        c_type = graph.nodes[c_id]["label_type"]
        if c_type in nodes and nodes[c_type] is None:
            nodes[c_type] = c_id
        else:
            nodes[f"__{index}__"] = c_id
            index += 1

    return nodes


def match_ast_d(
    graph: Graph,
    n_id: NId,
    label_type: str,
    depth: int = 1,
) -> NId | None:
    return match_ast(graph, n_id, label_type, depth=depth)[label_type]


def match_ast_group(
    graph: Graph,
    n_id: NId,
    *label_type: str,
    depth: int = 1,
) -> dict[str, list[NId]]:
    index: int = 0
    nodes: dict[str, list[NId]] = {label: [] for label in label_type}

    for c_id in adj_ast(graph, n_id, depth=depth):
        c_type = graph.nodes[c_id]["label_type"]
        if c_type in nodes:
            nodes[c_type].append(c_id)
        else:
            nodes[f"__{index}__"] = [
                c_id,
            ]
            index += 1

    return nodes


def match_ast_group_d(
    graph: Graph,
    n_id: str,
    label_type: str,
    depth: int = 1,
) -> list[str]:
    return match_ast_group(graph, n_id, label_type, depth=depth)[label_type]


def get_ast_childs(
    graph: Graph,
    n_id: NId,
    label_type: str,
    *,
    depth: int = 1,
) -> tuple[NId, ...]:
    return tuple(
        n_id
        for n_id in adj_ast(graph, n_id, depth=depth)
        if graph.nodes[n_id]["label_type"] == label_type
    )


def is_connected_to_cfg(graph: Graph, n_id: NId) -> bool:
    return bool(adj_cfg(graph, n_id) or pred_cfg(graph, n_id))


def lookup_first_cfg_parent(
    graph: Graph,
    n_id: NId,
) -> NId:
    # Lookup first parent who is connected to the CFG
    for p_id in chain([n_id], pred_ast_lazy(graph, n_id, depth=-1)):
        if is_connected_to_cfg(graph, p_id):
            return p_id
    # Base case, pass through
    return n_id


def import_graph_from_json(model: Any) -> Graph:
    graph = Graph()

    for n_id, n_attrs in model["nodes"].items():
        graph.add_node(n_id, **n_attrs)
        for csv_label in ("label_input_type", "label_sink_type"):
            if csv_label in graph.nodes[n_id]:
                graph.nodes[n_id][csv_label] = set(
                    graph.nodes[n_id][csv_label].split(",")
                )

    for n_id_from, n_id_from_value in model["edges"].items():
        for n_id_to, edge_attrs in n_id_from_value.items():
            graph.add_edge(n_id_from, n_id_to, **edge_attrs)

    return graph


def _add_csv_label(
    data: dict[str, Any], n_id: str, n_attrs: Any
) -> dict[str, Any]:
    data["nodes"][n_id] = n_attrs.copy()
    for csv_label in ("label_input_type", "label_sink_type"):
        if csv_label in data["nodes"][n_id]:
            data["nodes"][n_id][csv_label] = ",".join(
                sorted(data["nodes"][n_id][csv_label])
            )
    return data


def export_graph_as_json(
    graph: Graph,
    *,
    include_styles: bool = False,
) -> dict[str, Any]:
    data: dict[str, Any] = {}
    data["nodes"] = {}
    data["edges"] = {}
    ignored_attrs = GRAPH_STYLE_ATTRS

    for n_id, n_attrs in graph.nodes.items():
        data = _add_csv_label(data, n_id, n_attrs)

        if not include_styles:
            for attr in ignored_attrs:
                data["nodes"][n_id].pop(attr, None)

    for n_id_from, n_id_to in graph.edges:
        data["edges"].setdefault(n_id_from, {})
        data["edges"][n_id_from][n_id_to] = graph[n_id_from][n_id_to].copy()

        if not include_styles:
            for attr in ignored_attrs:
                data["edges"][n_id_from][n_id_to].pop(attr, None)

    return data


def _get_subgraph(
    graph: Graph,
    node_n_id_predicate: NIdPredicateFunction = lambda n_id: True,
    edge_n_attrs_predicate: NAttrsPredicateFunction = lambda n_attrs: True,
) -> Graph:
    copy: Graph = Graph()

    for n_a_id, n_b_id in graph.edges:
        edge_attrs = graph[n_a_id][n_b_id].copy()
        n_a_attrs = graph.nodes[n_a_id].copy()
        n_b_attrs = graph.nodes[n_b_id].copy()

        if (
            edge_n_attrs_predicate(edge_attrs)
            and node_n_id_predicate(n_a_id)
            and node_n_id_predicate(n_b_id)
        ):
            copy.add_node(n_a_id, **n_a_attrs)
            copy.add_node(n_b_id, **n_b_attrs)
            copy.add_edge(n_a_id, n_b_id, **edge_attrs)

    return copy


def copy_ast(graph: Graph) -> Graph:
    return _get_subgraph(
        graph=graph,
        edge_n_attrs_predicate=pred_has_labels(label_ast="AST"),
    )


def copy_cfg(graph: Graph) -> Graph:
    return _get_subgraph(
        graph=graph,
        edge_n_attrs_predicate=pred_has_labels(label_cfg="CFG"),
    )


def search_pred_until_type(
    graph: Graph,
    n_id: NId,
    targets: set[str],
    last_child: str | None = None,
) -> tuple[str, str | None]:
    if not last_child:
        last_child = n_id
    if pred_c := pred_ast(graph, n_id):
        if graph.nodes[pred_c[0]]["label_type"] in targets:
            return (pred_c[0], last_child)
        return search_pred_until_type(graph, pred_c[0], targets, pred_c[0])
    return "", ""


def get_nodes_by_path(
    graph: Graph, n_id: NId, nodes: list[NId], *label_type_path: str
) -> list[NId]:
    if len(label_type_path) == 1:
        nodes.extend(match_ast_group_d(graph, n_id, label_type_path[0]))
        return nodes
    for node in match_ast_group_d(graph, n_id, label_type_path[0]):
        get_nodes_by_path(graph, node, nodes, *label_type_path[1:])

    return nodes


def nodes_by_type(graph: Graph) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for node in graph:
        if label_type := graph.nodes[node].get("label_type"):
            if label_type not in result:
                result[label_type] = []
            result[label_type].append(node)
    return result


def prev_node_by_id(node_list: list[str], node_id: str) -> str:
    numbers_list = [int(x) for x in node_list]
    id_int = int(node_id)
    min_elem = id_int
    for elem in numbers_list:
        if elem < id_int:
            min_elem = elem
    return str(min_elem)
