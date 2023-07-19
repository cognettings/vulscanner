from collections.abc import (
    Iterator,
)
import ctx
from model.graph import (
    Graph,
    NId,
)
from symbolic_eval.types import (
    Path,
)
from utils import (
    graph as g,
)


def iter_ast(graph: Graph, n_id: NId, strict: bool = False) -> Iterator[NId]:
    if not strict or not g.is_connected_to_cfg(graph, n_id):
        yield n_id

    for c_id in g.adj_ast(graph, n_id):
        if strict and g.is_connected_to_cfg(graph, c_id):
            continue
        yield from iter_ast(graph, c_id)


def iter_backward_paths(graph: Graph, cfg_n_id: NId) -> Iterator[Path]:
    path = [cfg_n_id]
    parents = g.pred_cfg(graph, cfg_n_id)

    if not parents:
        yield path

    for parent in parents:
        for sub_path in iter_backward_paths(graph, parent):
            yield path + sub_path


def get_backward_paths(graph: Graph, n_id: NId) -> Iterator[Path]:
    cfg_id = g.lookup_first_cfg_parent(graph, n_id)
    paths_gen = iter_backward_paths(graph, cfg_id)
    if limit := ctx.SKIMS_CONFIG.sast.recursion_limit:
        it_count = 1
        while it_count < limit:
            try:
                yield next(paths_gen)
                it_count += 1
            except StopIteration:
                return
    else:
        yield from paths_gen


def iter_forward_paths(graph: Graph, cfg_id: NId) -> Iterator[Path]:
    path = [cfg_id]
    childs = g.adj_cfg(graph, cfg_id)

    if not childs:
        yield path

    for child in childs:
        for sub_path in iter_forward_paths(graph, child):
            yield path + sub_path


def get_forward_paths(graph: Graph, n_id: NId) -> Iterator[Path]:
    cfg_id = g.lookup_first_cfg_parent(graph, n_id)
    yield from iter_forward_paths(graph, cfg_id)


def invert_path(path: Path) -> Path:
    inv_path = path.copy()
    inv_path.reverse()
    return inv_path


def get_inv_forward_paths(graph: Graph, n_id: NId) -> Iterator[Path]:
    for path in get_forward_paths(graph, n_id):
        yield invert_path(path)


def filter_ast(
    graph: Graph, n_id: NId, types: set[str], strict: bool = False
) -> Iterator[NId]:
    for c_id in iter_ast(graph, n_id, strict):
        if graph.nodes[c_id]["label_type"] in types:
            yield c_id


def get_lookup_path(graph: Graph, path: Path, symbol_id: NId) -> Path:
    cfg_parent = g.lookup_first_cfg_parent(graph, symbol_id)
    cfg_parent_idx = path.index(cfg_parent)  # current instruction idx
    return path[cfg_parent_idx + 1 :]  # from previus instruction idx


def get_object_identifiers(graph: Graph, obj_names: set[str]) -> list[str]:
    identifiers = []
    for nid in g.matching_nodes(graph, label_type="ObjectCreation"):
        if (
            graph.nodes[nid].get("name") in obj_names
            and (pred := g.pred_ast(graph, nid)[0])
            and graph.nodes[pred].get("label_type") == "VariableDeclaration"
        ):
            identifiers.append(graph.nodes[pred].get("variable"))
    return identifiers


def get_value_member_access(
    graph: Graph, expression: str, member: str
) -> str | None:
    possible_types = {"Literal"}
    for nid in g.filter_nodes(
        graph,
        nodes=graph.nodes,
        predicate=g.pred_has_labels(
            label_type="MemberAccess",
            expression=expression,
            member=member,
        ),
    ):
        if (
            (pred := g.pred_ast(graph, nid)[0])
            and graph.nodes[pred].get("label_type") == "Assignment"
            and (value := list(g.match_ast(graph, pred).values())[1])
            and graph.nodes[value].get("label_type") in possible_types
        ):
            return value
    return None


def get_current_class(graph: Graph, n_id: str) -> NId:
    class_nodes = g.filter_nodes(
        graph, graph.nodes, g.pred_has_labels(label_type="Class")
    )
    nid_class: NId = g.prev_node_by_id(list(class_nodes), n_id)
    return nid_class
