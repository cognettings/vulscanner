from custom_parsers.types import (
    ListToken,
)
from lark import (
    Tree as LarkTree,
)
from lark.tree import (
    Meta as LarkMeta,
)
from metaloaders.model import (
    Node,
    Type,
)
from model import (
    core,
    cvss3,
    graph,
)
import safe_pickle
from safe_pickle import (
    dump,
    load,
)
from typing import (
    Any,
)
from utils.graph import (
    export_graph_as_json,
    import_graph_from_json,
)


def _dump_graph(instance: graph.Graph) -> safe_pickle.Serialized:
    graph_as_json = export_graph_as_json(instance, include_styles=True)
    return safe_pickle.serialize(instance, graph_as_json)


def _load_graph(graph_as_json: Any) -> graph.Graph:
    return import_graph_from_json(graph_as_json)


def _dump_lark_meta(meta: LarkMeta) -> safe_pickle.Serialized:
    return safe_pickle.serialize(
        meta,
        *map(
            safe_pickle.dump_raw,
            {
                attr: getattr(meta, attr, None)
                for attr in (
                    "column",
                    "empty",
                    "end_column",
                    "end_line",
                    "line",
                )
            },
        ),
    )


def _load_lark_meta(**kwargs: dict) -> LarkMeta:
    meta = LarkMeta()
    for attr, value in kwargs.items():
        if value is not None:
            setattr(meta, attr, value)
    return meta


def _dump_lark_tree(tree: LarkTree) -> safe_pickle.Serialized:
    return safe_pickle.serialize(
        tree,
        *map(
            safe_pickle.dump_raw,
            (
                tree.children,
                tree.data,
                tree.meta,
            ),
        ),
    )


def _load_lark_tree(children: Any, data: Any, meta: Any) -> LarkTree:
    return LarkTree(data, children, meta)


def _side_effects() -> None:
    for factory in (
        core.AvailabilityEnum,
        core.DeveloperEnum,
        core.ExecutionQueue,
        core.FindingEnum,
        core.MethodsEnum,
        core.MethodOriginEnum,
        core.Platform,
        core.TechniqueEnum,
        core.VulnerabilityKindEnum,
        core.VulnerabilityStateEnum,
        cvss3.AttackComplexity,
        cvss3.AttackVector,
        cvss3.AvailabilityImpact,
        cvss3.ConfidentialityImpact,
        cvss3.Exploitability,
        cvss3.IntegrityImpact,
        cvss3.PrivilegesRequired,
        cvss3.RemediationLevel,
        cvss3.ReportConfidence,
        cvss3.SeverityScope,
        cvss3.SeverityScope,
        cvss3.UserInteraction,
        graph.GraphShardMetadataLanguage,
        Type,
    ):
        safe_pickle.register_enum(factory)

    for factory in (  # type: ignore
        core.ExecutionQueueConfig,
        core.FindingMetadata,
        core.HTTPProperties,
        core.SkimsVulnerabilityMetadata,
        core.Vulnerability,
        cvss3.Score,
        graph.GraphDB,
        graph.GraphShardCacheable,
        graph.GraphShard,
        graph.GraphShardMetadata,
        Node,
    ):
        safe_pickle.register_namedtuple(factory)

    for factory, dumper, loader in (
        (graph.Graph, _dump_graph, _load_graph),
        (LarkMeta, _dump_lark_meta, _load_lark_meta),
        (LarkTree, _dump_lark_tree, _load_lark_tree),
        (ListToken, safe_pickle.tuple_dump, safe_pickle.list_load),
    ):
        safe_pickle.register(factory, dumper, loader)  # type: ignore


# Side effects
_side_effects()

# Exported members
__all__ = ["dump", "load"]
