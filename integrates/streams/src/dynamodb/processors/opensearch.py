from datetime import (
    datetime,
    timezone,
)
from dynamodb.context import (
    FI_AWS_OPENSEARCH_HOST,
    FI_ENVIRONMENT,
)
from dynamodb.resilience import (
    queue_dead_letter,
)
from dynamodb.resource import (
    SESSION,
)
from dynamodb.types import (
    Item,
    Record,
    StreamEvent,
)
from dynamodb.utils import (
    SetEncoder,
)
import logging
from opensearchpy import (
    AWSV4SignerAuth,
    OpenSearch,
    RequestsHttpConnection,
)
from opensearchpy.helpers import (
    bulk,
    BulkIndexError,
)

CREDENTIALS = SESSION.get_credentials()
CLIENT = OpenSearch(
    connection_class=RequestsHttpConnection,
    hosts=[FI_AWS_OPENSEARCH_HOST],
    http_auth=AWSV4SignerAuth(CREDENTIALS, SESSION.region_name),
    http_compress=True,
    max_retries=10,
    retry_on_status=(429, 502, 503, 504),
    retry_on_timeout=True,
    serializer=SetEncoder(),
    use_ssl=FI_ENVIRONMENT == "prod",
    verify_certs=FI_ENVIRONMENT == "prod",
)
LOGGER = logging.getLogger(__name__)


def _process(records: tuple[Record, ...], index: str) -> None:
    """Replicates the item on AWS OpenSearch"""
    actions: list[Item] = []

    for record in records:
        action_name = (
            "delete" if record.event_name == StreamEvent.REMOVE else "index"
        )
        action = {
            "_id": "#".join([record.pk, record.sk]),
            "_index": index,
            "_op_type": action_name,
        }
        if action_name == "index" and record.new_image:
            actions.append({**action, "_source": record.new_image})
        else:
            actions.append(action)

    try:
        bulk(client=CLIENT, actions=actions, ignore_status=(404,))
    except BulkIndexError as ex:
        LOGGER.exception(ex, extra={"extra": {"errors": ex.errors}})
        records_by_id = {
            "#".join([record.pk, record.sk]): record for record in records
        }
        for error in ex.errors:
            values = list(error.values())[0]
            record_id = values["_id"]
            record = records_by_id[record_id]
            queue_dead_letter(record, __name__)


def _format_vulns(records: tuple[Record, ...]) -> tuple[Record, ...]:
    formatted = []

    for record in records:
        if (
            record.event_name in {StreamEvent.INSERT, StreamEvent.MODIFY}
            and record.new_image
            and "hash" in record.new_image
        ):
            # Needed as it doesn't fit in OpenSearch long data type (2^63)
            record.new_image["hash"] = str(record.new_image["hash"])
        formatted.append(record)
    return tuple(formatted)


def _format_date(obj: dict, date_key: str) -> None:
    if date_key in obj and obj[date_key] is not None:
        obj[date_key] = (
            datetime.fromisoformat(obj[date_key])
            .astimezone(tz=timezone.utc)
            .isoformat()
        )


def _format_findings(records: tuple[Record, ...]) -> tuple[Record, ...]:
    formatted = []

    for record in records:
        ind_key = "unreliable_indicators"
        old_date_key = "oldest_vulnerability_report_date"
        new_date_key = "newest_vulnerability_report_date"

        if (
            record.event_name in {StreamEvent.INSERT, StreamEvent.MODIFY}
            and record.new_image
            and ind_key in record.new_image
        ):
            # Date must be in ISO format
            _format_date(record.new_image[ind_key], old_date_key)
            _format_date(record.new_image[ind_key], new_date_key)

        formatted.append(record)
    return tuple(formatted)


def process_vulns(records: tuple[Record, ...]) -> None:
    formatted = _format_vulns(records)
    _process(formatted, "vulnerabilities")


def process_findings(records: tuple[Record, ...]) -> None:
    formatted = _format_findings(records)
    _process(formatted, "findings")


def process_executions(records: tuple[Record, ...]) -> None:
    _process(records, "forces_executions")


def process_events(records: tuple[Record, ...]) -> None:
    _process(records, "events")


def process_lines(records: tuple[Record, ...]) -> None:
    _process(records, "toe_lines")
