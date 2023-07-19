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
    get_object_identifiers,
)
from utils import (
    graph as g,
)


def is_danger_value(
    graph: Graph, n_id: NId, memb_name: str, method_supplies: MethodSupplies
) -> bool:
    method = MethodsEnum.CS_WEAK_CREDENTIAL
    insec_rules = {
        "RequireDigit": ["false"],
        "RequireNonAlphanumeric": ["false"],
        "RequireUppercase": ["false"],
        "RequireLowercase": ["false"],
        "RequiredLength": ["0", "1", "2", "3", "4", "5", "6", "7"],
        "RequiredUniqueChars": ["0", "1", "2", "3", "4", "5"],
    }
    if not insec_rules.get(memb_name):
        return False

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
            and (results := list(evaluation.triggers))
            and len(results) > 0
            and results[0] in insec_rules[memb_name]
        ):
            return True
    return False


def get_weak_policies_ids(
    graph: Graph, n_id: NId, method_supplies: MethodSupplies
) -> set[NId]:
    weak_nodes: set[NId] = set()
    parent_id = g.pred(graph, n_id)[0]
    al_id = graph.nodes[parent_id].get("arguments_id")
    opt_id = g.match_ast(graph, al_id).get("__0__")
    if opt_id and graph.nodes[opt_id]["label_type"] == "MethodDeclaration":
        block_id = graph.nodes[opt_id]["block_id"]
        config_options = g.adj_ast(graph, block_id)
        for assignment in config_options:
            arg_list = g.adj_ast(graph, assignment)
            if (
                len(arg_list) >= 2
                and (memb_n := graph.nodes[arg_list[0]])
                and "Password" in memb_n.get("expression")
                and (member := memb_n.get("member"))
                and is_danger_value(
                    graph, arg_list[1], member, method_supplies
                )
            ):
                weak_nodes.add(arg_list[0])
    return weak_nodes


def check_no_password_argument(triggers: set[str]) -> bool:
    eval_str = "".join(list(triggers))
    for arg_part in eval_str.split(";"):
        if "=" in arg_part:
            var, value = arg_part.split("=", maxsplit=1)
            if var == "Password" and not value:
                return True
    return False


def get_eval_danger(
    method: MethodsEnum,
    graph: Graph,
    n_id: NId,
    method_supplies: MethodSupplies,
) -> bool:
    for path in get_backward_paths(graph, n_id):
        evaluation = evaluate(
            method, graph, path, n_id, method_supplies.graph_db
        )
        if evaluation and check_no_password_argument(evaluation.triggers):
            return True
    return False


# https://docs.microsoft.com/es-es/aspnet/core/security/authentication/identity-configuration
def c_sharp_weak_credential_policy(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        config_options = "Configure<IdentityOptions>"
        vuln_nodes: set[NId] = set()
        for node in method_supplies.selected_nodes:
            if graph.nodes[node].get("member") != config_options:
                continue
            vuln_nodes.update(
                get_weak_policies_ids(graph, node, method_supplies)
            )
        for n_id in vuln_nodes:
            yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_weak_credential_policy.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=MethodsEnum.CS_WEAK_CREDENTIAL,
    )


def c_sharp_no_password(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.CS_NO_PASSWORD
    bad_types = {"Microsoft", "EntityFrameworkCore", "DbContextOptionsBuilder"}

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        flagged_vars = get_object_identifiers(graph, bad_types)

        for node in method_supplies.selected_nodes:
            expr = graph.nodes[node].get("expression")
            parent_id = g.pred(graph, node)[0]
            if (
                expr in flagged_vars
                and graph.nodes[node].get("member") == "UseSqlServer"
                and (al_id := graph.nodes[parent_id].get("arguments_id"))
                and (test_nid := g.match_ast(graph, al_id).get("__0__"))
                and get_eval_danger(method, graph, test_nid, method_supplies)
            ):
                yield shard, node

    return get_vulnerabilities_from_n_ids(
        desc_key="src.lib_root.f035.csharp_no_password.description",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
