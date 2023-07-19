from collections.abc import (
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
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)


def get_eval_danger(graph: Graph, n_id: NId, method: MethodsEnum) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(method, graph, path, n_id)
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers
            != {
                "featureEntitisSetted",
                "featureParametterSetted",
                "featureDoctypeSetted",
            }
        ):
            return True
    return False


def kt_insecure_parser(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.KT_XML_PARSER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            member = graph.nodes[nid].get("member")
            object_id = graph.nodes[nid].get("expression_id")
            if (member == "parse") and get_eval_danger(
                graph, object_id, method
            ):
                yield shard, nid

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f083.generic_xml_parser",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_XML_PARSER,
    )
