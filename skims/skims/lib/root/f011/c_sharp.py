from collections.abc import (
    Iterable,
    Iterator,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    Graph,
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.utils import (
    get_object_identifiers,
)
from utils.graph import (
    adj_ast,
    match_ast_d,
)
from utils.string import (
    split_on_last_dot as split_last,
)


def is_insec_squema(
    graph: Graph, n_id: str, identifiers: Iterable[str]
) -> NId | None:
    split_expr = split_last(graph.nodes[n_id].get("expression"))
    if (
        split_expr[0] in identifiers
        and split_expr[1] == "Add"
        and (args := match_ast_d(graph, n_id, "ArgumentList"))
        and all(
            graph.nodes[_id]["label_type"] == "Literal"
            for _id in adj_ast(graph, args)
        )
    ):
        return args
    return None


def c_sharp_xsl_transform_object(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_XSL_TRANSFORM_OBJECT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("name") == "XslTransform":
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f011.csharp_xsl_transform_object",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def c_sharp_schema_by_url(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_SCHEMA_BY_URL

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            obj_identifiers = get_object_identifiers(
                graph, {"XmlSchemaCollection"}
            )
            if args := is_insec_squema(graph, node, obj_identifiers):
                yield shard, args

    return get_vulnerabilities_from_n_ids(
        desc_key="f011.c_sharp_schema_by_url",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
