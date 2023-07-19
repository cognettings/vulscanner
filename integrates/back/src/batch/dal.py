import aioboto3
from aioextensions import (
    collect,
    in_thread,
)
import aiohttp
import asyncio
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    JobStatus,
    Product,
    SkimsBatchQueue,
)
from batch.types import (
    AttributesNoOverridden,
    BatchProcessing,
    Job,
    PutActionResult,
)
import boto3
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    ClientError,
    CredentialRetrievalError,
    ParamValidationError,
)
from collections.abc import (
    Callable,
)
from context import (
    CACHIX_AUTH_TOKEN,
    FI_ASYNC_PROCESSING_DB_MODEL_PATH,
    FI_AWS_REGION_NAME,
    FI_ENVIRONMENT,
    UNIVERSE_API_TOKEN,
)
from custom_utils.datetime import (
    get_as_epoch,
    get_now,
)
from custom_utils.encodings import (
    safe_encode,
)
from datetime import (
    datetime,
)
from dynamodb import (
    operations as dynamodb_ops,
)
from dynamodb.tables import (
    load_tables,
)
from dynamodb.types import (
    SimpleKey,
)
import hashlib
import hmac
from itertools import (
    chain,
    product,
)
import json
import logging
import logging.config
import math
import more_itertools
from more_itertools.recipes import (
    flatten,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
)
from urllib.parse import (
    urlparse,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)
OPTIONS = dict(
    region_name=FI_AWS_REGION_NAME,
    service_name="batch",
)
TABLE_NAME: str = "fi_async_processing"


with open(
    FI_ASYNC_PROCESSING_DB_MODEL_PATH, mode="r", encoding="utf-8"
) as file:
    TABLE = load_tables(json.load(file))[0]


def to_queue(
    raw: str, fluid_product: Product
) -> IntegratesBatchQueue | SkimsBatchQueue:
    if fluid_product is Product.INTEGRATES:
        return IntegratesBatchQueue(raw.lower())
    return SkimsBatchQueue(raw.lower())


def mapping_to_key(items: list[str]) -> str:
    key = ".".join(
        [safe_encode(attribute_value) for attribute_value in sorted(items)]
    )
    return hashlib.sha256(key.encode()).hexdigest()


async def list_queues_jobs(
    queues: list[IntegratesBatchQueue],
    statuses: list[JobStatus],
    *,
    filters: tuple[Callable[[Job], bool], ...] = (),
) -> list[Job]:
    if FI_ENVIRONMENT == "development":
        return []
    return list(
        chain.from_iterable(
            await collect(
                [
                    _list_queue_jobs(queue, status, filters=filters)
                    for queue, status in product(queues, statuses)
                ]
            )
        )
    )


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _get_signature_key(
    key: str, date_stamp: str, region_name: str, service_name: str
) -> bytes:
    k_date = _sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region_name)
    k_service = _sign(k_region, service_name)
    k_signing = _sign(k_service, "aws4_request")
    return k_signing


async def list_jobs(  # pylint: disable=too-many-locals
    queue: IntegratesBatchQueue,
    next_token: str | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    service = "batch"
    session = boto3.Session()
    credentials = session.get_credentials()
    client = session.client(service)
    endpoint = f"{client.meta.endpoint_url}/v1/listjobs"
    method = "POST"
    host = urlparse(endpoint).hostname or ""
    region = client.meta.region_name
    content_type = "application/x-amz-json-1.0"
    amz_target = "Batch_20120810.ListJobs"
    request_parameters = {
        "jobQueue": queue.value,
        **kwargs,
    }
    if next_token:
        request_parameters["nextToken"] = next_token

    request_parameters_str = json.dumps(request_parameters)
    access_key = credentials.access_key
    secret_key = credentials.secret_key
    time = datetime.utcnow()
    amz_date = time.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = time.strftime("%Y%m%d")

    canonical_uri = "/v1/listjobs"
    canonical_querystring = ""
    canonical_headers = (
        "content-type:"
        + content_type
        + "\n"
        + "host:"
        + host
        + "\n"
        + "x-amz-date:"
        + amz_date
        + "\n"
        + "x-amz-target:"
        + amz_target
        + "\n"
    )
    signed_headers = "content-type;host;x-amz-date;x-amz-target"
    payload_hash = hashlib.sha256(
        request_parameters_str.encode("utf-8")
    ).hexdigest()

    canonical_request = (
        method
        + "\n"
        + canonical_uri
        + "\n"
        + canonical_querystring
        + "\n"
        + canonical_headers
        + "\n"
        + signed_headers
        + "\n"
        + payload_hash
    )
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = (
        date_stamp + "/" + region + "/" + service + "/" + "aws4_request"
    )
    string_to_sign = (
        algorithm
        + "\n"
        + amz_date
        + "\n"
        + credential_scope
        + "\n"
        + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    )
    signing_key = _get_signature_key(secret_key, date_stamp, region, service)
    signature = hmac.new(
        signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256
    ).hexdigest()
    authorization_header = (
        algorithm
        + " "
        + "Credential="
        + access_key
        + "/"
        + credential_scope
        + ", "
        + "SignedHeaders="
        + signed_headers
        + ", "
        + "Signature="
        + signature
    )
    headers = {
        "Content-Type": content_type,
        "X-Amz-Date": amz_date,
        "X-Amz-Target": amz_target,
        "Authorization": authorization_header,
    }
    retries = 0
    async with aiohttp.ClientSession(headers=headers) as session:
        retry = True
        while retry and retries < 100:
            retry = False
            async with session.post(
                endpoint, data=request_parameters_str
            ) as response:
                try:
                    result = await response.json()
                except json.decoder.JSONDecodeError:
                    break
                if (
                    not response.ok
                    and result.get("message", "") == "Too Many Requests"
                ):
                    retry = True
                    retries += 1
                    await asyncio.sleep(0.1)
                    continue
                return result
    return {}


async def _get_all_jobs(**kwargs: Any) -> list[dict[str, Any]]:
    _response = await list_jobs(**kwargs)
    for _job in _response["jobSummaryList"]:
        _job["jobQueue"] = kwargs.get("queue")

    result = _response["jobSummaryList"]

    if _next_token := _response.get("nextToken"):
        kwargs["nextToken"] = _next_token
        result.extend(await _get_all_jobs(**kwargs))
    return result


async def list_jobs_by_group(
    queue: IntegratesBatchQueue, group: str
) -> list[dict[str, Any]]:
    return await _get_all_jobs(
        queue=queue,
        filters=[
            {"name": "JOB_NAME", "values": [f"skims-execute-machine-{group}*"]}
        ],
    )


async def list_jobs_by_status(
    queue: IntegratesBatchQueue, status: str
) -> list[dict[str, Any]]:
    return await _get_all_jobs(queue=queue, jobStatus=status)


async def list_log_streams(
    group: str, *job_ids: str
) -> list[dict[str, str | int]]:
    options = OPTIONS.copy()
    options.update({"service_name": "logs"})

    async with aioboto3.Session().client(**options) as cloudwatch:

        async def _request(
            _job_id: str | None = None, next_token: str | None = None
        ) -> list[dict[str, Any]]:
            _response = await cloudwatch.describe_log_streams(
                logGroupName="skims",
                logStreamNamePrefix=f"{group}/{_job_id}/"
                if _job_id
                else f"{group}/",
                **({"nextToken": next_token} if next_token else {}),
            )
            result: list[dict[str, Any]] = _response["logStreams"]

            if _next_token := _response.get("nextToken"):
                result.extend(await _request(_job_id, next_token=_next_token))
            return result

        if job_ids:
            return list(
                more_itertools.flatten(
                    await collect(_request(_job_id) for _job_id in job_ids)
                )
            )
        return await _request()


async def describe_jobs(*job_ids: str) -> tuple[dict[str, Any], ...]:
    if not job_ids:
        return ()

    async with aioboto3.Session().client(**OPTIONS) as batch:
        return tuple(
            flatten(
                response["jobs"]
                for response in await collect(
                    tuple(
                        batch.describe_jobs(jobs=list(_set_jobs))
                        for _set_jobs in more_itertools.divide(
                            math.ceil(len(job_ids) / 100), job_ids
                        )
                    )
                )
            )
        )


async def _list_queue_jobs(
    queue: IntegratesBatchQueue,
    status: JobStatus,
    *,
    filters: tuple[Callable[[Job], bool], ...],
) -> list[Job]:
    client = boto3.client("batch")
    results: list[Job] = []

    async def _request(next_token: str | None = None) -> str | None:
        response = await in_thread(
            client.list_jobs,
            jobQueue=queue.value,
            jobStatus=status.name,
            **(dict(nextToken=next_token) if next_token else {}),
        )

        for job_summary in response.get("jobSummaryList", []):
            job = Job(
                created_at=job_summary.get("createdAt"),
                exit_code=job_summary.get("container", {}).get("exitCode"),
                exit_reason=job_summary.get("container", {}).get("reason"),
                id=job_summary["jobId"],
                name=job_summary["jobName"],
                queue=queue.value,
                started_at=job_summary.get("startedAt"),
                stopped_at=job_summary.get("stoppedAt"),
                status=status.name,
            )
            if all(filter_(job) for filter_ in filters):
                results.append(job)

        return response.get("nextToken")

    next_token = await _request()
    while next_token:
        next_token = await _request(next_token)

    return results


async def delete_action(
    *,
    action_name: str | None = None,
    additional_info: str | None = None,
    entity: str | None = None,
    subject: str | None = None,
    time: str | None = None,
    dynamodb_pk: str | None = None,
) -> bool:
    try:
        if dynamodb_pk:
            key = dynamodb_pk
        elif action_name and additional_info and entity and subject and time:
            key = generate_key_to_dynamod(
                action_name=action_name,
                additional_info=additional_info,
                entity=entity,
                subject=subject,
            )
        else:
            raise Exception(
                "you must supply the dynamodb pk argument"
                " or any other arguments to build pk"
            )
        await dynamodb_ops.delete_item(
            key=SimpleKey(partition_key=key),
            table=TABLE,
        )

        return True
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))

    return False


async def is_action_by_key(*, key: str) -> bool:
    item = await dynamodb_ops.get_item(
        facets=(TABLE.facets["action_metadata"],),
        key=SimpleKey(partition_key=key),
        table=TABLE,
    )

    return bool(item)


async def get_action(
    *,
    action_dynamo_pk: str,
) -> BatchProcessing | None:
    item = await dynamodb_ops.get_item(
        facets=(TABLE.facets["action_metadata"],),
        key=SimpleKey(partition_key=action_dynamo_pk),
        table=TABLE,
    )
    if item is None:
        return None

    return BatchProcessing(
        key=item["pk"],
        action_name=item["action_name"].lower(),
        entity=item["entity"].lower(),
        subject=item["subject"].lower(),
        time=item["time"],
        additional_info=item.get("additional_info", ""),
        queue=item["queue"],
        batch_job_id=item.get("batch_job_id"),
        retries=item.get("retries", 0),
        running=item.get("running", False),
    )


async def get_actions_by_name(
    action_name: str, entity: str
) -> tuple[BatchProcessing, ...]:
    index = TABLE.indexes["gsi-1"]
    response = await dynamodb_ops.query(
        condition_expression=(
            Key(index.primary_key.partition_key).eq(action_name)
            & Key(index.primary_key.sort_key).eq(entity)
        ),
        facets=(TABLE.facets["action_metadata"],),
        table=TABLE,
        index=index,
    )

    return tuple(
        BatchProcessing(
            key=item["pk"],
            action_name=item["action_name"].lower(),
            entity=item["entity"].lower(),
            subject=item["subject"].lower(),
            time=item["time"],
            additional_info=item.get("additional_info", ""),
            queue=item["queue"],
            batch_job_id=item.get("batch_job_id"),
            retries=item.get("retries", 0),
            running=item.get("running", False),
        )
        for item in response.items
    )


async def get_actions() -> list[BatchProcessing]:
    items = await dynamodb_ops.scan(table=TABLE)

    return [
        BatchProcessing(
            key=item["pk"],
            action_name=item["action_name"].lower(),
            entity=item["entity"].lower(),
            subject=item["subject"].lower(),
            time=item["time"],
            additional_info=item.get("additional_info", ""),
            queue=item["queue"],
            batch_job_id=item.get("batch_job_id"),
            retries=item.get("retries", 0),
            running=item.get("running", False),
        )
        for item in items
    ]


def generate_key_to_dynamod(
    *,
    action_name: str,
    additional_info: str,
    entity: str,
    subject: str,
) -> str:
    return mapping_to_key(
        [
            action_name,
            additional_info,
            entity,
            subject,
        ]
    )


async def put_action_to_dynamodb(
    *,
    action_name: str,
    entity: str,
    subject: str,
    time: str,
    additional_info: str,
    queue: IntegratesBatchQueue | SkimsBatchQueue,
    batch_job_id: str | None = None,
    key: str | None = None,
) -> str | None:
    try:
        key = key or generate_key_to_dynamod(
            action_name=action_name,
            additional_info=additional_info,
            entity=entity,
            subject=subject,
        )
        item = dict(
            pk=key,
            action_name=action_name,
            additional_info=additional_info,
            entity=entity,
            subject=subject,
            time=time,
            queue=queue.value,
            batch_job_id=batch_job_id,
        )
        await dynamodb_ops.put_item(
            facet=TABLE.facets["action_metadata"],
            item=item,
            table=TABLE,
        )

        return key
    except ClientError as exc:
        LOGGER.exception(exc, extra=dict(extra=locals()))

    return None


async def update_action_to_dynamodb(*, key: str, **kwargs: Any) -> bool:
    no_update_attributes = {
        "action_name",
        "entity",
        "subject",
        "time",
        "queue",
    }
    has_bad = no_update_attributes.intersection(set(kwargs.keys()))
    if has_bad:
        raise AttributesNoOverridden(*has_bad)

    key_structure = TABLE.primary_key
    condition_expression = Attr(key_structure.partition_key).exists()
    try:
        await dynamodb_ops.update_item(
            condition_expression=condition_expression,
            item=kwargs,
            key=SimpleKey(partition_key=key),
            table=TABLE,
        )

        return True
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})

    return False


async def put_action_to_batch(
    *,
    action_name: str,
    action_dynamo_pk: str,
    entity: str,
    product_name: str,
    queue: IntegratesBatchQueue | SkimsBatchQueue,
    attempt_duration_seconds: int = 3600,
    memory: int = 3800,
    vcpus: int = 1,
    **kwargs: Any,
) -> str | None:
    if FI_ENVIRONMENT == "development":
        return None
    try:
        command_name = f"/{product_name}/batch"
        if action_name == "clone_roots":
            command_name = "/integrates/jobs/clone_roots"
        if action_name == "execute-machine":
            command_name = "/integrates/jobs/execute_machine"

        async with aioboto3.Session().client(**OPTIONS) as batch:
            return (
                await batch.submit_job(
                    jobName=f"{product_name}-{action_name}-{entity}",
                    jobQueue=queue.value,
                    jobDefinition="prod_integrates",
                    containerOverrides={
                        "command": [
                            "m",
                            "gitlab:fluidattacks/universe@trunk",
                            command_name,
                            "prod",
                            action_dynamo_pk,
                        ],
                        "environment": [
                            {
                                "name": "CACHIX_AUTH_TOKEN",
                                "value": CACHIX_AUTH_TOKEN,
                            },
                            {
                                "name": "CI",
                                "value": "true",
                            },
                            {
                                "name": "MAKES_AWS_BATCH_COMPAT",
                                "value": "true",
                            },
                            {
                                "name": "UNIVERSE_API_TOKEN",
                                "value": UNIVERSE_API_TOKEN,
                            },
                        ],
                        "resourceRequirements": [
                            {"type": "MEMORY", "value": str(memory)},
                            {"type": "VCPU", "value": str(vcpus)},
                        ],
                    },
                    retryStrategy={
                        "attempts": 1,
                    },
                    timeout={
                        "attemptDurationSeconds": attempt_duration_seconds
                    },
                    **kwargs,
                )
            )["jobId"]
    except (
        ClientError,
        ParamValidationError,
        CredentialRetrievalError,
    ) as exc:
        LOGGER.exception(
            exc,
            extra=dict(
                extra=dict(
                    action_name=action_name,
                    action_dynamo_pk=action_dynamo_pk,
                )
            ),
        )
        return None


async def cancel_batch_job(
    *, job_id: str, reason: str = "not required"
) -> None:
    if FI_ENVIRONMENT == "development":
        return None
    try:
        async with aioboto3.Session().client(**OPTIONS) as batch:
            await batch.cancel_job(jobId=job_id, reason=reason)
    except ClientError as exc:
        LOGGER.exception(
            exc,
            extra=dict(extra=None),
        )


async def terminate_batch_job(
    *, job_id: str, reason: str = "not required"
) -> None:
    if FI_ENVIRONMENT == "development":
        return None
    try:
        async with aioboto3.Session().client(**OPTIONS) as batch:
            await batch.terminate_job(jobId=job_id, reason=reason)
    except ClientError as exc:
        LOGGER.exception(
            exc,
            extra=dict(extra=None),
        )


async def put_action(
    *,
    action: Action,
    additional_info: str,
    entity: str,
    product_name: Product,
    subject: str,
    queue: IntegratesBatchQueue | SkimsBatchQueue,
    attempt_duration_seconds: int = 3600,
    dynamodb_pk: str | None = None,
    vcpus: int = 1,
    **kwargs: Any,
) -> PutActionResult:
    time: str = str(get_as_epoch(get_now()))
    possible_key = dynamodb_pk or generate_key_to_dynamod(
        action_name=action.value,
        additional_info=additional_info,
        entity=entity,
        subject=subject,
    )
    if (
        current_action := await get_action(action_dynamo_pk=possible_key)
    ) and (not current_action.running):
        LOGGER.info(
            "There is a job that is still in queue for %s",
            entity,
        )
        return PutActionResult(
            success=False,
            batch_job_id=current_action.batch_job_id,
            dynamo_pk=dynamodb_pk,
        )

    if dynamo_pk := await put_action_to_dynamodb(
        key=possible_key,
        action_name=action.value,
        entity=entity,
        subject=subject,
        time=time,
        additional_info=additional_info,
        queue=queue,
    ):
        job_id = await put_action_to_batch(
            action_name=action.value,
            vcpus=vcpus,
            queue=queue,
            entity=entity,
            attempt_duration_seconds=attempt_duration_seconds,
            action_dynamo_pk=possible_key,
            product_name=product_name.value,
            **kwargs,
        )
        await update_action_to_dynamodb(key=dynamo_pk, batch_job_id=job_id)

        LOGGER.info(
            "A job for %s has been queued",
            entity,
        )
        return PutActionResult(
            success=True,
            batch_job_id=job_id,
            dynamo_pk=dynamo_pk,
        )
    return PutActionResult(
        success=False,
        dynamo_pk=possible_key,
    )
