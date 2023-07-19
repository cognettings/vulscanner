from collections.abc import (
    Callable,
)
from model.graph import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
    NId,
)
from typing import (
    Any,
    NamedTuple,
    NotRequired,
    TypedDict,
)

SYNTAX_GRAPH_ARGS = Any  # pylint: disable=invalid-name


class SyntaxMetadata(TypedDict):
    class_path: list[str]


class SyntaxGraphArgs(NamedTuple):
    generic: Callable[[SYNTAX_GRAPH_ARGS], NId]
    path: str
    language: GraphLanguage
    ast_graph: Graph
    syntax_graph: Graph
    n_id: NId
    metadata: SyntaxMetadata

    def fork_n_id(self, n_id: NId) -> SYNTAX_GRAPH_ARGS:
        return SyntaxGraphArgs(
            generic=self.generic,
            path=self.path,
            language=self.language,
            ast_graph=self.ast_graph,
            syntax_graph=self.syntax_graph,
            n_id=n_id,
            metadata=self.metadata,
        )


SyntaxReader = Callable[[SyntaxGraphArgs], NId]


class Dispatcher(NamedTuple):
    applicable_types: set[str]
    syntax_reader: SyntaxReader


Dispatchers = tuple[Dispatcher, ...]


class MissingSyntaxReader(Exception):
    pass


class MissingCaseHandling(Exception):
    pass


class FileStructData(TypedDict):
    node: NId
    node_range: NotRequired[list[NId]]
    type: str
    data: dict | str


class FileInstanceData(TypedDict):
    object: str
    package: str
