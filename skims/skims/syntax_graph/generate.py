from model.graph import (
    Graph,
    GraphShardMetadataLanguage as GraphLanguage,
)
from syntax_graph.dispatchers import (
    DISPATCHERS_BY_LANG,
)
from syntax_graph.syntax_readers.common.missing_node import (
    reader as missing_node_reader,
)
from syntax_graph.types import (
    MissingCaseHandling,
    MissingSyntaxReader,
    SyntaxGraphArgs,
    SyntaxMetadata,
)
from typing import (
    cast,
)
from utils.logs import (
    log_blocking,
)


def generic(args: SyntaxGraphArgs) -> str:
    node_type = args.ast_graph.nodes[args.n_id]["label_type"]
    if lang_dispatchers := DISPATCHERS_BY_LANG.get(args.language):
        for dispatcher in lang_dispatchers:
            if node_type in dispatcher.applicable_types:
                return dispatcher.syntax_reader(args)

    log_blocking(
        "debug",
        f"Missing syntax reader for {node_type} in {args.language.name}",
    )

    return missing_node_reader(args, node_type)


def build_syntax_graph(
    path: str,
    language: GraphLanguage,
    ast_graph: Graph,
    with_metadata: bool,
) -> Graph:
    syntax_graph = Graph()

    syntax_metadata = SyntaxMetadata(class_path=[])

    if with_metadata:
        syntax_graph.add_node(
            "0",
            label_type="Metadata",
            structure={},
            instances={},
            imports=[],
            path=path,
        )

    try:
        generic(
            SyntaxGraphArgs(
                generic,
                path,
                language,
                ast_graph,
                syntax_graph,
                "1",
                syntax_metadata,
            )
        )
    except (MissingSyntaxReader, MissingCaseHandling) as error:
        log_blocking("warning", cast(str, error))
    return syntax_graph
