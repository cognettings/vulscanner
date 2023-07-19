from collections.abc import (
    Callable,
)
from model.graph import (
    GraphShard,
    GraphShardMetadataLanguage as ShardLanguage,
)


def set_context_java(shard: GraphShard, context: dict) -> None:
    if shard.metadata.package:
        if shard.metadata.language not in context:
            context[shard.metadata.language] = {}

        ctx_java = context[shard.metadata.language]

        file_struct = shard.syntax_graph.nodes["0"]["structure"]

        if shard.metadata.package in ctx_java:
            ctx_java[shard.metadata.package][shard.path] = file_struct
        else:
            ctx_java[shard.metadata.package] = {shard.path: file_struct}


CONTEXT_SETTERS: dict[ShardLanguage, Callable[[GraphShard, dict], None]] = {
    ShardLanguage.JAVA: set_context_java
}


def set_context_by_lang(shard: GraphShard, context: dict) -> None:
    if context_setter := CONTEXT_SETTERS.get(shard.metadata.language):
        context_setter(shard, context)
