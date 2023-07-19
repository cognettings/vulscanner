from model.graph import (
    Graph,
)
from utils import (
    graph as g,
)


def library_is_imported(graph: Graph, lib_name: str) -> bool:
    def predicate_matcher(node: dict[str, str]) -> bool:
        return bool(
            (node.get("label_type") == "Import")
            and (n_exp := node.get("module"))
            and (n_exp == lib_name)
        )

    return bool(g.filter_nodes(graph, graph.nodes, predicate_matcher))


def process_from_statement(node: dict, lib_name: str) -> str | None:
    if (
        (module := node.get("module"))
        and (imp_value := node.get("imported_value"))
        and (f"{module}.{imp_value}" == lib_name)
    ):
        if alias := node.get("imported_alias"):
            return alias
        return lib_name
    return None


def get_alias(graph: Graph, lib_name: str) -> set[str]:
    imported_names: set[str] = set()
    nodes = graph.nodes
    for n_id in g.matching_nodes(graph, label_type="Import"):
        if nodes[n_id].get("imported_value"):
            if imported_name := process_from_statement(nodes[n_id], lib_name):
                imported_names.add(imported_name)
        elif nodes[n_id].get("module") == lib_name:
            if alias := nodes[n_id].get("imported_alias"):
                imported_names.add(alias)
            else:
                imported_names.add(lib_name)
    return imported_names


def get_danger_imported_names(graph: Graph, lib_names: set[str]) -> set[str]:
    danger_callings: set[str] = set()
    for lib_name in lib_names:
        tokens = lib_name.split(".")

        for token in range(1, len(tokens) + 1):
            main_name = ".".join(tokens[:token])
            trailing_name = ".".join(tokens[token:])

            for imported_name in get_alias(graph, main_name):
                if trailing_name:
                    imported_name += f".{trailing_name}"
                danger_callings.add(imported_name)

    return danger_callings
