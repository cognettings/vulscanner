import boto3
from botocore.exceptions import (
    ClientError,
)
from dynamodb.context import (
    FI_ENVIRONMENT,
)
from dynamodb.types import (
    Record,
)
import json
import logging
import sys

LOGGER = logging.getLogger(__name__)


def queue_dead_letter(record: Record, processor_name: str) -> None:
    if FI_ENVIRONMENT != "prod":
        return

    client = boto3.client("sqs")

    message = json.dumps(
        {
            "id": "#".join([record.pk, record.sk]),
            "processor_name": processor_name,
            "record": record,
        },
        default=str,
    )
    if sys.getsizeof(message) > 2084:
        message = json.dumps(
            {
                "id": "#".join([record.pk, record.sk]),
                "processor_name": processor_name,
                "record": dict(
                    _message=(
                        "The record exceeds the 2048 bytes"
                        " so only new image is send"
                    ),
                    operation=record.event_name,
                    new_image=record.new_image,
                ),
            },
            default=str,
        )
    try:
        client.send_message(
            QueueUrl=(
                "https://sqs.us-east-1.amazonaws.com/205810638802/"
                "integrates_streams_dlq"
            ),
            MessageBody=message,
        )
    except ClientError as error:
        LOGGER.error(
            error,
            extra=dict(
                extra=dict(
                    operation=record.event_name,
                    process=processor_name,
                    record_id="#".join([record.pk, record.sk]),
                )
            ),
        )
