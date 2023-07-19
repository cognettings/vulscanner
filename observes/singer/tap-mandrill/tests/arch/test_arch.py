from .arch import (
    forbidden_allowlist,
    project_dag,
    raise_or_return,
)
from arch_lint.dag.check import (
    check_dag_map,
    dag_map_completeness,
)
from arch_lint.forbidden import (
    check_forbidden,
)
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)
from arch_lint.private import (
    check_private,
)

root = raise_or_return(FullPathModule.from_raw("tap_mandrill"))


def test_dag_creation() -> None:
    project_dag()


def test_dag() -> None:
    graph = ImportGraph.from_modules(root, False)
    check_dag_map(project_dag(), graph)


def test_dag_completeness() -> None:
    graph = ImportGraph.from_modules(root, False)
    dag_map_completeness(project_dag(), graph, root)


def test_forbidden_creation() -> None:
    forbidden_allowlist()


def test_forbidden() -> None:
    graph = ImportGraph.from_modules(root, True)
    allowlist_map = forbidden_allowlist()
    check_forbidden(allowlist_map, graph)


def test_private() -> None:
    graph = ImportGraph.from_modules(root, False)
    check_private(graph, root)
