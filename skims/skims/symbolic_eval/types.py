from collections.abc import (
    Callable,
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
    Vulnerability,
)
from model.graph import (
    Graph,
    GraphDB,
    GraphShard,
    NId,
)
from typing import (
    Any,
    NamedTuple,
)
from xmlrpc.client import (
    boolean,
)

Path = list[NId]

SYMBOLIC_EVAL_ARGS = Any  # pylint: disable=invalid-name


class SymbolicEvaluation(NamedTuple):
    danger: boolean
    triggers: set[str]


class SymbolicEvalArgs(NamedTuple):
    generic: Callable[[SYMBOLIC_EVAL_ARGS], SymbolicEvaluation]
    method: MethodsEnum
    evaluation: dict[NId, bool]
    graph: Graph
    path: Path
    n_id: NId
    triggers: set[str]
    graph_db: GraphDB | None

    def fork_n_id(
        self, n_id: NId, path: Path | None = None, graph: Graph | None = None
    ) -> SYMBOLIC_EVAL_ARGS:
        if not path:
            path = self.path
        if not graph:
            graph = self.graph
        return SymbolicEvalArgs(
            generic=self.generic,
            method=self.method,
            evaluation=self.evaluation,
            triggers=self.triggers,
            graph=graph,
            path=path,
            n_id=n_id,
            graph_db=self.graph_db,
        )

    def fork(self, **attrs: Any) -> SYMBOLIC_EVAL_ARGS:
        params = self._asdict()
        params.update(attrs)
        return SymbolicEvalArgs(**params)


Analyzer = Callable[[GraphShard], Vulnerabilities]
LanguageAnalyzer = Callable[[GraphShard], Iterator[Vulnerability]]
Evaluator = Callable[[SymbolicEvalArgs], SymbolicEvaluation]


class MissingSymbolicEval(Exception):
    pass


class BadMethodInvocation(Exception):
    pass


class MissingAnalizer(Exception):
    pass


class MissingLanguageAnalizer(Exception):
    pass
