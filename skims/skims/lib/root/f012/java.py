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
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from symbolic_eval.evaluate import (
    evaluate,
)
from symbolic_eval.utils import (
    get_backward_paths,
)
from utils import (
    graph as g,
)
from utils.string import (
    complete_attrs_on_set,
)

# Constants
WS = r"\s*"
SEP = f"{WS},{WS}"


def has_like_injection(statement: str) -> bool:
    roots = (
        # like %x
        r"like\s+%{}",
        # like x%
        r"like\s+{}%",
        # like %x%
        r"like\s+%{}%",
        # like concat('%',   x)
        rf"like\s+concat\('%'{SEP}{{}}\)",
        # like concat(x,  '%')
        rf"like\s+concat\({{}}{SEP}'%'\)",
        # like concat('%',   x,'%')
        rf"like\s+concat\('%'{SEP}{{}}{SEP}'%'\)",
    )
    variables = (
        # :#{[0]}
        r":\#\{\[\d+\]\}",
        # :lastname
        r":[a-z0-9_\$]+",
        # ?0
        r"\?\d+",
    )
    statement = statement.lower()

    for var in variables:
        for root in roots:
            if re.search(root.format(var), statement):
                return True
    return False


def is_argument_vuln(
    method: MethodsEnum,
    graph: Graph,
    n_id: NId,
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        if (
            (
                evaluation := evaluate(
                    method,
                    graph,
                    path,
                    n_id,
                    graph_db=method_supplies.graph_db,
                )
            )
            and (stmt := "".join(list(evaluation.triggers)))
            and has_like_injection(stmt)
        ):
            return True
    return False


def analyze_jpa_node(
    method: MethodsEnum,
    graph: Graph,
    annotation_id: str,
    method_supplies: MethodSupplies,
) -> bool:
    _, *c_ids = g.adj_ast(graph, annotation_id, depth=2)
    results_vuln = []
    for n_id in c_ids:
        results_vuln.append(
            is_argument_vuln(method, graph, n_id, method_supplies)
        )

    if any(results_vuln):
        m_id = g.pred_ast(graph, annotation_id, depth=2)[1]
        pm_id = g.adj_ast(graph, m_id, label_type="ParameterList")[0]
        annotations = g.adj_ast(graph, pm_id, depth=3, label_type="Annotation")
        if not any(
            graph.nodes[annotation]["name"] == "Bind"
            for annotation in annotations
        ):
            return True
    return False


def java_jpa_like(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JAVA_JPA_LIKE
    danger_decorators = complete_attrs_on_set(
        {
            "org.springframework.data.jpa.repository.Query",
            "org.springframework.jdbc.object.SqlQuery",
        }
    )

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for node in method_supplies.selected_nodes:
            identifier_text = graph.nodes[node]["name"]
            if identifier_text in danger_decorators and analyze_jpa_node(
                method, graph, node, method_supplies
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="f012.java_jpa_like",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
