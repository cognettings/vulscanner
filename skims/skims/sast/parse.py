from collections.abc import (
    Iterator,
)
from ctx import (
    TREE_SITTER_PARSERS,
)
from itertools import (
    count,
)
import json
from model.graph import (
    Graph,
    GraphDB,
    GraphShard,
    GraphShardCacheable,
    GraphShardMetadata,
    GraphShardMetadataLanguage,
    GraphSyntax,
)
import os
from sast import (
    SUPPORTED_MULTIFILE,
)
from sast.context import (
    set_context_by_lang,
)
from syntax_cfg.generate import (
    add_syntax_cfg,
)
from syntax_graph.generate import (
    build_syntax_graph,
)
from tree_sitter import (
    Language,
    Node,
    Parser,
    Tree,
)
from utils.encodings import (
    json_dump,
)
from utils.fs import (
    decide_language,
    safe_sync_get_file_raw_content,
)
from utils.graph import (
    copy_ast,
    styles,
    to_svg,
)
from utils.logs import (
    log_blocking,
)
from utils.string import (
    get_debug_path,
)


class ParsingError(Exception):
    pass


FIELDS_BY_LANGUAGE: dict[
    GraphShardMetadataLanguage, dict[str, tuple[str, ...]]
] = {}


def _get_fields_by_language() -> None:
    for lang in GraphShardMetadataLanguage:
        if lang == GraphShardMetadataLanguage.NOT_SUPPORTED:
            continue

        path: str = os.path.join(
            TREE_SITTER_PARSERS, f"{lang.value}-fields.json"
        )

        with open(path, encoding="utf-8") as file:
            FIELDS_BY_LANGUAGE[lang] = json.load(file)


_get_fields_by_language()


def hash_node(node: Node) -> int:
    return hash((node.end_point, node.start_point, node.type))


def _is_final_node(node: Node, language: GraphShardMetadataLanguage) -> bool:
    return (
        (
            language == GraphShardMetadataLanguage.CSHARP
            and node.type
            in {
                "string_literal",
                "boolean_literal",
                "character_literal",
                "integer_literal",
                "null_literal",
                "real_literal",
                "verbatim_string_literal",
                "this_expression",
                "assignment_operator",
            }
        )
        or (
            language == GraphShardMetadataLanguage.DART
            and node.type
            in {
                "decimal_floating_point_literal",
                "decimal_integer_literal",
                "false",
                "hex_integer_literal",
                "list_literal",
                "null_literal",
                "set_or_map_literal",
                "string_literal",
                "symbol_literal",
                "true",
            }
        )
        or (
            language == GraphShardMetadataLanguage.GO
            and node.type
            in {
                "interface_type",
                "interpreted_string_literal",
            }
        )
        or (
            language == GraphShardMetadataLanguage.JAVA
            and node.type
            in {
                "array_type",
                "character_literal",
                "field_access",
                "floating_point_type",
                "generic_type",
                "integral_type",
                "scoped_identifier",
                "scoped_type_identifier",
                "this",
                "type_identifier",
            }
        )
        or (
            language == GraphShardMetadataLanguage.JAVASCRIPT
            and node.type
            in {
                "this",
                "super",
                "number",
                "string",
                "template_string",
                "regex",
                "true",
                "false",
                "null",
                "undefined",
            }
        )
        or (
            language == GraphShardMetadataLanguage.PHP
            and node.type
            in {
                "named_type",
            }
        )
        or (
            language == GraphShardMetadataLanguage.RUBY
            and node.type in {"scope_resolution"}
        )
        or (
            language == GraphShardMetadataLanguage.TYPESCRIPT
            and node.type
            in {
                "this",
                "super",
                "number",
                "string",
                "template_string",
                "regex",
                "true",
                "false",
                "null",
                "undefined",
            }
        )
        or (
            language == GraphShardMetadataLanguage.KOTLIN
            and node.type in {"boolean_literal", "line_string_literal"}
        )
        or (
            language == GraphShardMetadataLanguage.PYTHON
            and node.type in {"string", "integer", "float", "true", "false"}
        )
    )


def _build_ast_graph(
    content: bytes,
    language: GraphShardMetadataLanguage,
    node: Node,
    counter: Iterator[str],
    graph: Graph,
    *,
    _edge_index: str | None = None,
    _parent: str | None = None,
    _parent_fields: dict[int, str] | None = None,
) -> Graph:
    if not isinstance(node, Node):
        raise NotImplementedError()

    if node.has_error:
        raise ParsingError()

    n_id = next(counter)
    raw_l, raw_c = node.start_point

    graph.add_node(
        n_id, label_l=raw_l + 1, label_c=raw_c + 1, label_type=node.type
    )

    if _parent is not None:
        graph.add_edge(_parent, n_id, label_ast="AST", label_index=_edge_index)

        # if the node is a parent field acording node_type file, associate id
        # example node-types files at https://github.com/
        # tree-sitter/tree-sitter-c-sharp/blob/master/src/node-types.json
        # tree-sitter/tree-sitter-java/blob/master/src/node-types.json
        if field := (_parent_fields or {}).get(hash_node(node)):
            graph.nodes[_parent][f"label_field_{field}"] = n_id

    if not node.children or _is_final_node(node, language):
        # Consider it a final node, extract the text from it
        node_content = content[node.start_byte : node.end_byte]
        graph.nodes[n_id]["label_text"] = node_content.decode("latin-1")

    elif language != GraphShardMetadataLanguage.NOT_SUPPORTED:
        # It's not a final node, recurse
        for edge_index, child in enumerate(node.children):
            _build_ast_graph(
                content,
                language,
                child,
                counter,
                graph,
                _edge_index=str(edge_index),
                _parent=n_id,
                _parent_fields={
                    hash_node(child): fld
                    for fld in FIELDS_BY_LANGUAGE[language].get(node.type, ())
                    for child in [node.child_by_field_name(fld)]
                    if child
                },
            )

    return graph


def parse_content(
    content: bytes,
    language: GraphShardMetadataLanguage,
) -> Tree:
    path: str = os.path.join(TREE_SITTER_PARSERS, f"{language.value}.so")
    parser: Parser = Parser()
    parser.set_language(Language(path, language.value))
    return parser.parse(content)


def _parse_one_cached(
    *,
    content: bytes,
    path: str,
    language: GraphShardMetadataLanguage,
    with_metadata: bool,
    debug_mode: bool,
) -> GraphShardCacheable | None:
    raw_tree: Tree = parse_content(content, language)
    node: Node = raw_tree.root_node

    counter = map(str, count(1))
    try:
        graph: Graph = _build_ast_graph(
            content, language, node, counter, Graph()
        )
    except ParsingError:
        return None

    if syntax_graph := build_syntax_graph(
        path, language, graph, with_metadata
    ):
        syntax_graph = add_syntax_cfg(syntax_graph)

    syntax: GraphSyntax = {}

    metadata_package = None
    if metadata_node := syntax_graph.nodes.get("0"):
        metadata_package = metadata_node.get("package")

    metadata = GraphShardMetadata(language=language, package=metadata_package)

    if debug_mode:
        styles.add(graph)
        if syntax_graph:
            styles.add(syntax_graph)

    return GraphShardCacheable(
        graph=graph,
        metadata=metadata,
        syntax=syntax,
        syntax_graph=syntax_graph,
    )


def parse_one(
    path: str,
    language: GraphShardMetadataLanguage,
    content: bytes | None = None,
    with_metadata: bool = False,
    debug_mode: bool = False,
) -> GraphShard | None:
    if not content:
        return None
    try:
        graph = _parse_one_cached(
            content=content,
            path=path,
            language=language,
            with_metadata=with_metadata,
            debug_mode=debug_mode,
        )
    except (
        ArithmeticError,
        AttributeError,
        BufferError,
        EOFError,
        LookupError,
        MemoryError,
        NameError,
        OSError,
        ReferenceError,
        RuntimeError,
        SystemError,
        TypeError,
        ValueError,
        ParsingError,
    ) as err:
        log_blocking("warning", "Error while parsing: %s, ignoring", path)
        log_blocking("warning", type(err))
        log_blocking("warning", err)
        return None

    if not graph:
        return None

    if debug_mode:
        output = get_debug_path("tree-sitter-" + path)
        to_svg(copy_ast(graph.graph), f"{output}.ast")
        if graph.syntax_graph:
            to_svg(graph.syntax_graph, f"{output}.syntax_graph")

    return GraphShard(
        graph=graph.graph,
        metadata=graph.metadata,
        path=path,
        syntax=graph.syntax,
        syntax_graph=graph.syntax_graph,
    )


def _get_content(path: str, working_dir: str) -> bytes | None:
    full_path = os.path.join(working_dir, path)
    return safe_sync_get_file_raw_content(full_path)


def parse_many(
    paths: tuple[str, ...],
    working_dir: str,
    debug_mode: bool = False,
) -> Iterator[GraphShard]:
    for path in paths:
        if (
            (language := decide_language(path))
            and (language in SUPPORTED_MULTIFILE)
            and (content := _get_content(path, working_dir))
            and (
                parsed := parse_one(path, language, content, True, debug_mode)
            )
        ):
            yield parsed


def get_graph_db(
    paths: tuple[str, ...], working_dir: str, debug_mode: bool = False
) -> GraphDB:
    # Reproducibility
    paths = tuple(sorted(paths))

    graph_db = GraphDB(
        context={},
        shards={},
        shards_by_language_class={},
        shards_by_path={},
    )

    for index, shard in enumerate(
        parse_many(paths, working_dir, debug_mode), start=1
    ):
        set_context_by_lang(shard, graph_db.context)
        graph_db.shards.update({shard.path: shard})
        graph_db.shards_by_path[shard.path] = index - 1

    if debug_mode:
        output = get_debug_path("tree-sitter")
        with open(f"{output}.json", "w", encoding="utf-8") as handle:
            json_dump(graph_db, handle, indent=2, sort_keys=True)

    return graph_db


def get_shard(
    path: str,
    language: GraphShardMetadataLanguage,
    working_dir: str,
    debug_mode: bool = False,
) -> GraphShard | None:
    graph_shard = (
        parse_one(
            path, language, _get_content(path, working_dir), False, debug_mode
        )
        if language != GraphShardMetadataLanguage.NOT_SUPPORTED
        else None
    )

    if graph_shard and debug_mode:
        output = get_debug_path("tree-sitter")
        with open(f"{output}.json", "w", encoding="utf-8") as handle:
            json_dump(graph_shard, handle, indent=2, sort_keys=True)

    return graph_shard
