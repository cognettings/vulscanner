from collections.abc import (
    Iterator,
)
from lib.root.utilities.kubernetes import (
    check_template_integrity,
    get_key_value,
)
from model.core import (
    MethodsEnum,
    Vulnerabilities,
)
from model.graph import (
    GraphShard,
    GraphShardNode,
    MethodSupplies,
    NId,
)
import re
from sast.query import (
    get_vulnerabilities_from_n_ids,
)
from utils.graph import (
    match_ast_group_d,
)


def _image_has_digest(value: str, nid: NId) -> NId | None:
    env_var_re: re.Pattern = re.compile(r"\{.+\}")
    digest_re: re.Pattern = re.compile(".*@sha256:[a-fA-F0-9]{64}")
    if not (env_var_re.search(value) or digest_re.search(value)):
        return nid
    return None


def k8s_image_has_digest(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.K8S_IMAGE_HAS_DIGEST

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if not check_template_integrity(graph, nid):
                return
            for p_id in match_ast_group_d(graph, nid, "Pair", depth=-1):
                key, value = get_key_value(graph, p_id)
                if key == "image" and (
                    report := _image_has_digest(value, p_id)
                ):
                    yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="lib_path.f426.k8s_image_has_digest",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
