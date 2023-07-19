from collections.abc import (
    Iterator,
)
from lib.root.utilities.terraform import (
    get_argument,
    get_attribute,
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


def _azure_app_service_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    if logs := get_argument(graph, nid, "logs"):
        fail_key, fail_val, _ = get_attribute(
            graph, logs, "failed_request_tracing_enabled"
        )
        det_key, det_val, _ = get_attribute(
            graph, logs, "detailed_error_messages_enabled"
        )
        if (not fail_key or fail_val.lower() == "false") or (
            not det_key or det_val.lower() == "false"
        ):
            return logs
    else:
        return nid
    return None


def _azure_sql_server_audit_log_retention(
    graph: Graph, nid: NId
) -> NId | None:
    if logs := get_argument(graph, nid, "extended_auditing_policy"):
        ret_key, ret_val, attr_id = get_attribute(
            graph, logs, "retention_in_days"
        )
        if not ret_key:
            return logs
        if ret_val.isdigit() and int(ret_val) <= 90:
            return attr_id
    else:
        return nid
    return None


def _azure_storage_logging_disabled(graph: Graph, nid: NId) -> NId | None:
    if queue := get_argument(graph, nid, "queue_properties"):
        if logging := get_argument(graph, queue, "logging"):
            attrs = [
                get_attribute(graph, logging, req)
                for req in ["delete", "read", "write"]
            ]
            if not all(
                (
                    val.lower() == "true" if req else False
                    for req, val, _ in attrs
                )
            ):
                return logging
        else:
            return queue
    else:
        return nid
    return None


def tfm_azure_storage_logging_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_STORAGE_LOG_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_storage_account" and (
                report := _azure_storage_logging_disabled(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f402.tfm_azure_storage_logging_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_sql_server_audit_log_retention(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_SQL_LOG_RETENT

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_sql_server" and (
                report := _azure_sql_server_audit_log_retention(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f402.tfm_azure_sql_server_audit_log_retention",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )


def tfm_azure_app_service_logging_disabled(
    shard: GraphShard, method_supplies: MethodSupplies
) -> Vulnerabilities:
    method = MethodsEnum.TFM_AZURE_APP_LOG_DISABLED

    def n_ids() -> Iterator[GraphShardNode]:
        graph = shard.syntax_graph
        for nid in method_supplies.selected_nodes:
            if graph.nodes[nid].get("name") == "azurerm_app_service" and (
                report := _azure_app_service_logging_disabled(graph, nid)
            ):
                yield shard, report

    return get_vulnerabilities_from_n_ids(
        desc_key="f402.tfm_azure_failed_request_tracing_disabled",
        desc_params={},
        graph_shard_nodes=n_ids(),
        method=method,
    )
