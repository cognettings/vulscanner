import base64
import json
import logging
import os
import requests
from time import (
    sleep,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

LOGGER = logging.getLogger()
HANDLER = LOGGER.handlers[0]
HANDLER.setFormatter(
    logging.Formatter(
        "[%(levelname)s] %(message)s",
    )
)


BETTER_UPTIME_API_TOKEN = os.environ["BETTER_UPTIME_API_TOKEN"]
GITLAB_API_TOKEN = os.environ["GITLAB_API_TOKEN"]
MAIN_BRANCH = "trunk"

Item = dict[str, Any]


def api_cancel_pipeline(project_id: str, pipeline_id: str) -> Item:
    headers = {"PRIVATE-TOKEN": GITLAB_API_TOKEN}
    for _ in range(3):
        response = requests.post(
            (
                f"https://gitlab.com/api/v4/projects/{project_id}/"
                f"pipelines/{pipeline_id}/cancel"
            ),
            headers=headers,
            timeout=30,
        )
        if response.status_code == 409:
            sleep(5)
        else:
            break

    data: Item = response.json()
    if response.status_code != 200:
        LOGGER.error(
            "failed to cancel pipeline %s with message: %s",
            pipeline_id,
            data.get("message", "unknown error"),
        )

    return data


def api_list_user_merge_requests(project_id: str, username: str) -> List[Item]:
    headers = {
        "PRIVATE-TOKEN": GITLAB_API_TOKEN,
    }
    params = {
        "state": "opened",
        "author_username": username,
    }

    response = requests.get(
        f"https://gitlab.com/api/v4/projects/{project_id}/merge_requests",
        params=params,
        headers=headers,
        timeout=30,
    )

    return response.json()


def api_list_merge_request_pipelines(
    project_id: str, merge_request_iid: str
) -> List[Item]:
    headers = {"PRIVATE-TOKEN": GITLAB_API_TOKEN}
    response = requests.get(
        (
            f"https://gitlab.com/api/v4/projects/{project_id}"
            f"/merge_requests/{merge_request_iid}/pipelines"
        ),
        headers=headers,
        timeout=30,
    )
    return response.json()


def api_list_user_running_pipelines(
    project_id: str, username: str
) -> List[Item]:
    headers = {
        "PRIVATE-TOKEN": GITLAB_API_TOKEN,
    }
    params = {
        "status": "running",
        "username": username,
        "ref": username,
    }

    response = requests.get(
        f"https://gitlab.com/api/v4/projects/{project_id}/pipelines",
        params=params,
        headers=headers,
        timeout=30,
    )
    return response.json()


def process_merge_request(
    project_id: str, pipeline_id: str, merge_request_iid: str
) -> bool:
    pipelines = api_list_merge_request_pipelines(
        project_id=project_id, merge_request_iid=merge_request_iid
    )
    pipelines = [
        pipeline for pipeline in pipelines if pipeline["source"] == "push"
    ]

    pipeline_to_cancel = next(
        (
            pipeline
            for pipeline in pipelines[:-1]
            if pipeline["status"]
            not in (
                "failed",
                "canceled",
                "skipped",
                "manual",
                "success",
                "scheduled",
                "pending",
            )
            and pipeline["id"] == pipeline_id
        ),
        None,
    )
    return bool(pipeline_to_cancel)


def pipeline_is_cancelable(
    *, project_id: str, pipeline_id: str, username: str
) -> Optional[bool]:
    # return an optional bool, it will only be a bool if there are MR available
    user_merge_requests = api_list_user_merge_requests(project_id, username)
    if not user_merge_requests:
        LOGGER.info(
            "could not associate an MR to the pipeline %s", pipeline_id
        )

    for merge_request in user_merge_requests:
        cancelable = process_merge_request(
            project_id=project_id,
            merge_request_iid=merge_request["iid"],
            pipeline_id=pipeline_id,
        )
        if cancelable:
            return True
    if user_merge_requests:
        return False

    return None


def review_branch(project_id: str, username: str) -> None:
    pipelines = api_list_user_running_pipelines(project_id, username)
    for pipeline in pipelines[1:]:
        response = api_cancel_pipeline(
            project_id=project_id, pipeline_id=pipeline["id"]
        )
        if response.get("status") or "message" not in response:
            LOGGER.warning(
                "pipeline canceled %s -> %s",
                pipeline["id"],
                response.get("status", "unknown status"),
            )


def process_pipeline(request_body: Item) -> Item:
    pipeline_id: str = request_body["object_attributes"]["id"]
    LOGGER.info("processing pipeline %s", pipeline_id)

    # if a job contains testPullRequest pipeline should not be canceled
    if (
        request_body["object_attributes"]["status"]
        in (
            "failed",
            "canceled",
            "skipped",
            "manual",
            "success",
            "scheduled",
        )
        or request_body["object_attributes"]["ref"] == MAIN_BRANCH
        or any(
            "/testPullRequest/" in build["name"]
            for build in request_body["builds"]
        )
    ):
        message = f"It is not necessary to cancel it {pipeline_id}"
        LOGGER.info(message)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(
                {
                    "message": message,
                }
            ),
        }

    cancelable = pipeline_is_cancelable(
        project_id=request_body["project"]["id"],
        pipeline_id=pipeline_id,
        username=request_body["object_attributes"]["ref"],
    )
    if cancelable:
        response = api_cancel_pipeline(
            request_body["project"]["id"], pipeline_id
        )
        if response.get("status") or "message" not in response:
            LOGGER.warning(
                "pipeline canceled %s -> %s",
                pipeline_id,
                response.get("status", "unknown status"),
            )

    elif cancelable is False:
        LOGGER.info("It is not necessary to cancel it %s", pipeline_id)
    else:
        review_branch(
            project_id=request_body["project"]["id"],
            username=request_body["object_attributes"]["ref"],
        )

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": "pipeline canceled"}),
    }


def get_status_pages() -> List[Item]:
    return requests.get(
        "https://betteruptime.com/api/v2/status-pages",
        headers={"Authorization": f"Bearer {BETTER_UPTIME_API_TOKEN}"},
        timeout=30,
    ).json()["data"]


def get_incident_severity(severity: str) -> str:
    if severity in ["critical", "high"]:
        return "downtime"

    return "degraded"


def get_affected_products(
    status_page_id: str, request_body: Item
) -> List[Item]:
    labels = request_body["object_attributes"]["labels"]
    names = {
        "airs": "WEB",
        "docs": "DOCS",
        "forces": "AGENT",
        "integrates": "ARM",
        "integrates-api": "API",
        "skims": "MACHINE",
    }
    internal_names = [
        label["title"].split("::")[1]
        for label in labels
        if label["title"].startswith("product::")
    ]
    public_names = [
        names[internal_name]
        for internal_name in internal_names
        if internal_name in names
    ]

    if not public_names:
        return []

    resources = requests.get(
        "https://uptime.betterstack.com/api/v2"
        f"/status-pages/{status_page_id}/resources",
        headers={"Authorization": f"Bearer {BETTER_UPTIME_API_TOKEN}"},
        timeout=30,
    ).json()["data"]
    return [
        {
            "status_page_resource_id": resource["id"],
            "status": (
                "resolved"
                if request_body["object_attributes"]["escalation_status"]
                == "resolved"
                else get_incident_severity(
                    request_body["object_attributes"]["severity"]
                )
            ),
        }
        for resource in resources
        if resource["attributes"]["public_name"] in public_names
    ]


def get_incident_status(status: str) -> str:
    statuses = {
        "triggered": "Investigating",
        "acknowledged": "Identified",
        "resolved": "Resolved",
    }
    return statuses[status]


def create_incident(status_page_id: str, request_body: Item) -> None:
    affected_products = get_affected_products(status_page_id, request_body)

    if not affected_products:
        return

    status = get_incident_status(
        request_body["object_attributes"]["escalation_status"]
    )
    requests.post(
        "https://uptime.betterstack.com/api/v2"
        f"/status-pages/{status_page_id}/status-reports",
        headers={"Authorization": f"Bearer {BETTER_UPTIME_API_TOKEN}"},
        json={
            "affected_resources": affected_products,
            "message": (
                f"[{status}] "
                + request_body["object_attributes"]["description"].strip(".")
                + ". Details in "
                + request_body["object_attributes"]["url"]
            ),
            "title": (
                f"[{request_body['object_attributes']['iid']}] "
                + request_body["object_attributes"]["title"]
            ),
        },
        timeout=30,
    )


def get_incident(status_page_id: str, request_body: Item) -> Optional[Item]:
    issue_id = request_body["object_attributes"]["iid"]
    status_reports = requests.get(
        "https://uptime.betterstack.com/api/v2"
        f"/status-pages/{status_page_id}/status-reports",
        headers={"Authorization": f"Bearer {BETTER_UPTIME_API_TOKEN}"},
        timeout=30,
    ).json()["data"]
    return next(
        (
            report
            for report in status_reports
            if report["attributes"]["title"].startswith(f"[{issue_id}]")
        ),
        None,
    )


def update_incident_title(
    status_page_id: str, status_report_id: str, request_body: Item
) -> None:
    requests.patch(
        "https://uptime.betterstack.com/api/v2"
        f"/status-pages/{status_page_id}/status-reports/{status_report_id}",
        headers={"Authorization": f"Bearer {BETTER_UPTIME_API_TOKEN}"},
        json={
            "title": (
                f"[{request_body['object_attributes']['iid']}] "
                + request_body["object_attributes"]["title"]
            ),
        },
        timeout=30,
    )


def update_incident(
    status_page_id: str, status_report_id: str, request_body: Item
) -> None:
    affected_products = get_affected_products(status_page_id, request_body)

    if not affected_products:
        return

    status = get_incident_status(
        request_body["object_attributes"]["escalation_status"]
    )
    requests.post(
        "https://uptime.betterstack.com/api/v2"
        f"/status-pages/{status_page_id}"
        f"/status-reports/{status_report_id}/status-updates",
        headers={"Authorization": f"Bearer {BETTER_UPTIME_API_TOKEN}"},
        json={
            "affected_resources": affected_products,
            "message": (
                f"[{status}] "
                + request_body["object_attributes"]["description"].strip(".")
                + ". Details in "
                + request_body["object_attributes"]["url"]
            ),
        },
        timeout=30,
    )


def process_issue(request_body: Item) -> Item:
    issue_id: str = request_body["object_attributes"]["id"]
    LOGGER.info("processing issue %s", issue_id)
    is_incident = "escalation_status" in request_body["object_attributes"]

    if is_incident:
        action = request_body["object_attributes"]["action"]
        status_page_id = get_status_pages()[0]["id"]

        if action == "open":
            create_incident(status_page_id, request_body)
        elif action == "update":
            incident = get_incident(status_page_id, request_body)

            if incident:
                status_report_id = incident["id"]
                title_changed = (
                    incident["attributes"]["title"].split("] ", maxsplit=1)[1]
                    != request_body["object_attributes"]["title"]
                )
                if title_changed:
                    update_incident_title(
                        status_page_id, status_report_id, request_body
                    )

                update_incident(status_page_id, status_report_id, request_body)
            else:
                create_incident(status_page_id, request_body)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": "issue processed"}),
    }


def handle(event: Dict[str, str], _context: object) -> Item:
    request_body: dict[str, object] = (
        json.loads(base64.b64decode(event["body"]).decode("unicode-escape"))
        if event["isBase64Encoded"]
        else json.loads(event["body"])
    )
    object_kind = request_body["object_kind"]

    if object_kind == "pipeline":
        return process_pipeline(request_body)
    if object_kind == "issue":
        return process_issue(request_body)

    LOGGER.error("unsupported object_kind: %s", object_kind)
    return {
        "statusCode": 400,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": "unsupported object_kind"}),
    }
