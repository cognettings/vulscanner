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


def get_eval_danger(
    graph: Graph,
    n_id: NId,
    method: MethodsEnum,
    method_supplies: MethodSupplies,
) -> bool:
    safe_opt1 = {
        "featureEntitisSetted",
        "featureParametterSetted",
        "featureDoctypeSetted",
    }
    safe_opt2 = {
        "externaldtd",
        "externalschema",
    }
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(
            method, graph, path, n_id, method_supplies.graph_db
        )
        if (
            evaluation
            and evaluation.danger
            and evaluation.triggers not in [safe_opt1, safe_opt2]
        ):
            return True
    return False


def java_insecure_parser(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_XML_PARSER

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            expression = graph.nodes[node].get("expression")
            object_id = graph.nodes[node].get("object_id")
            if (expression == "parse") and get_eval_danger(
                graph, object_id, method, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f083.generic_xml_parser",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.JAVA_XML_PARSER,
    )
