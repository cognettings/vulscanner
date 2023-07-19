from collections.abc import (
    Iterator,
)
from lib.root.f371.common import (
    has_set_inner_html,
)
from model import (
    core,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
)
from sast.query import (
    get_vulnerabilities_from_n_ids,
)


def uses_innerhtml(
    shard: GraphShard, method_supplies: MethodSupplies
) -> core.Vulnerabilities:
    method = core.MethodsEnum.JS_USES_INNERHTML

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if graph.nodes[n_id].get("expression") == "innerHTML":
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f371.generic_uses_innerhtml",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def js_bypass_security_trust_url(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_BYPASS_SECURITY_TRUST_URL
    risky_methods = {
        "bypassSecurityTrustHtml",
        "bypassSecurityTrustScript",
        "bypassSecurityTrustStyle",
        "bypassSecurityTrustUrl",
        "bypassSecurityTrustResourceUrl",
    }

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if graph.nodes[n_id]["expression"] in risky_methods:
                yield shard, n_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f371.bypass_security_trust",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def js_dangerously_set_innerhtml(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.JS_USES_DANGEROUSLY_SET_HTML

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for n_id in method_supplies.selected_nodes:
            if c_id := has_set_inner_html(graph, n_id):
                yield shard, c_id

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_root.f371.has_dangerously_set_innerhtml",
        desc_params=dict(lang="Jsx"),
        graph_shard_nodes=n_ids(),
        method=method,
    )
