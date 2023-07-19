"""Singer tap for the Timedoctor API."""

import argparse
import datetime
import json
import os
import re
import sys
from tap_timedoctor import (
    logs,
)
from tap_timedoctor.api import (
    Options,
    Worker,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)
import unicodedata
from urllib import (
    request,
)
import uuid

# Type aliases that improve clarity
JSON = Any

_TYPE_STRING: JSON = {"type": "string"}
_TYPE_NUMBER: JSON = {"type": "number"}
_TYPE_DATE: JSON = {"type": "string", "format": "date-time"}


def standard_name(name: str) -> str:
    """Remove heading and trailing whitespaces.

    Puts exactly one space between words and get rid of ñ and accent marks.
    """
    unic = unicodedata.normalize
    std = " ".join(name.split())
    std = (unic("NFKD", std).encode("ASCII", "ignore")).lower().decode("utf-8")
    return std


def ensure_200(status_code: Optional[int]) -> None:
    """Ensure status_code 200 or exit."""
    if status_code != 200:
        print(f"INFO: Timedoctor API, ERROR {status_code}")
        print("          The service is probably down.")
        print("         You should run this script again later.")
        sys.exit(1)


def translate_date(date_obj: Any) -> str:
    """Translate a date-time value to RFC3339 format."""
    date_obj = str(date_obj)
    if re.match(r"\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}\.\d+", date_obj):
        date_obj = datetime.datetime.strptime(
            date_obj, "%Y-%m-%dT%H:%M:%S.%fZ"
        )
    elif re.match(r"\d{4}.\d{2}.\d{2}.\d{2}.\d{2}.\d{2}", date_obj):
        date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%dT%H:%M:%S")
    elif isinstance(date_obj, (int, float)):
        date_obj = datetime.datetime.utcfromtimestamp(date_obj)
    else:
        try:
            date_obj = datetime.datetime.utcfromtimestamp(int(date_obj))
        except ValueError:
            date_obj = datetime.datetime(1900, 1, 1, 0, 0, 0)

    return date_obj.strftime("%Y-%m-%dT%H:%M:%SZ")


def sync_worklogs(
    api_worker: Worker,
    company_id: str,
    users_list: List[List[str]],
    start_date_str: str,
    end_date_str: str,
) -> None:
    """API version 1.0.

    https://api2.timedoctor.com/#/Activity/getActivityWorklog
    """

    # Convert str to date for needed date handling
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")

    def write_schema() -> None:
        """Write the schema for this table."""
        schema: JSON = {
            "type": "SCHEMA",
            "stream": "worklogs",
            "key_properties": ["worklog_id"],
            "schema": {
                "properties": {
                    "worklog_id": _TYPE_STRING,
                    "length": _TYPE_NUMBER,
                    "user_id": _TYPE_STRING,
                    "user_name": _TYPE_STRING,
                    "task_id": _TYPE_STRING,
                    "task_name": _TYPE_STRING,
                    "project_id": _TYPE_STRING,
                    "project_name": _TYPE_STRING,
                    "start_time": _TYPE_DATE,
                    "end_time": _TYPE_DATE,
                    "edited": _TYPE_STRING,
                    "work_mode": _TYPE_STRING,
                }
            },
        }
        logs.log_json_obj("worklogs.stdout", schema)
        logs.stdout_json_obj(schema)

    def write_records(user_id: str, user_name: str) -> None:
        """Write the records for this table."""

        def translate_work_mode(work_mode: str) -> str:
            """Translate new api values to keep using
            the values from the old api.
            """
            work_mode_map: JSON = {
                "offline": "offline or afk",
                "offcomputer": "offline or afk",
                "computer": "online",
                "mobile": "mobile app",
                "manual": "manually added",
                "break": "on break",
                "paidBreak": "on break",
                "unpaidBreak": "on break",
            }
            work_mode_str: str = work_mode_map.get(work_mode, "other")
            return work_mode_str

        worklogs: List = []
        interval_start_date = start_date

        # Can't get too many worklogs at once as it results in an error
        # so as a workaround we use a loop with a 5 day interval
        # until the end_date is reached
        while True:
            interval_end_date = interval_start_date + datetime.timedelta(
                days=5
            )

            # The end_date argument in the api is exclusive
            if interval_end_date >= end_date:
                interval_end_date = end_date + datetime.timedelta(days=1)

            # Convert date to str to prevent errors in get_worklogs
            interval_start_date_str = datetime.datetime.strftime(
                interval_start_date, "%Y-%m-%d"
            )
            interval_end_date_str = datetime.datetime.strftime(
                interval_end_date, "%Y-%m-%d"
            )

            (status_code, response) = api_worker.get_worklogs(
                company_id,
                user_id,
                Options(0, interval_start_date_str, interval_end_date_str),
            )
            ensure_200(status_code)

            response_obj: JSON = json.loads(response)
            logs.log_json_obj("worklogs", response_obj)

            worklogs = worklogs + response_obj.get("data", [])[0]

            interval_start_date = interval_end_date
            if interval_end_date > end_date:
                break

        for worklog in worklogs:
            start_time = translate_date(worklog.get("start", ""))
            end_time = datetime.datetime.strptime(
                start_time, "%Y-%m-%dT%H:%M:%SZ"
            ) + datetime.timedelta(seconds=worklog.get("time", 0))
            record: JSON = {
                "type": "RECORD",
                "stream": "worklogs",
                "record": {
                    "worklog_id": str(uuid.uuid4()),
                    "length": worklog.get("time", 0),
                    "user_id": worklog.get("userId", ""),
                    "user_name": standard_name(user_name),
                    "task_id": worklog.get("taskId", ""),
                    "task_name": worklog.get("taskName", ""),
                    "project_id": worklog.get("projectId", ""),
                    "project_name": worklog.get("projectName", ""),
                    "start_time": start_time,
                    "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "edited": "1"
                    if worklog.get("mode", "") == "manual"
                    else "0",
                    "work_mode": translate_work_mode(worklog.get("mode", "")),
                },
            }

            logs.log_json_obj("worklogs.stdout", record)
            logs.stdout_json_obj(record)

    write_schema()
    for user_id, user_name in users_list:
        write_records(user_id, user_name)


def _get_nested_value(obj: JSON, keys: List[str]) -> JSON:
    for key in keys:
        obj = obj.get(key, None) if isinstance(obj, dict) else obj
    return obj


def sync_computer_activity(
    api_worker: Worker,
    company_id: str,
    users_list: List[List[str]],
    project_dict: Dict[str, str],
    options: Options,
) -> None:
    """Sync computer activity using API version 1.0.

    https://api2.timedoctor.com/#/Files/getTypeFiles
    """

    # Adding a day to end_date because the argument in the api is exclusive
    adjusted_end_date = options.end_date

    if isinstance(options.end_date, str):
        end_date = datetime.datetime.strptime(
            options.end_date, "%Y-%m-%d"
        ) + datetime.timedelta(days=1)
        adjusted_end_date = datetime.datetime.strftime(end_date, "%Y-%m-%d")

    def write_schema() -> None:
        """Write the schema for this table."""
        schema: JSON = {
            "type": "SCHEMA",
            "stream": "computer_activity",
            "key_properties": ["uuid"],
            "schema": {
                "properties": {
                    "uuid": _TYPE_STRING,
                    "date": _TYPE_DATE,
                    "user_id": _TYPE_STRING,
                    "user_name": _TYPE_STRING,
                    "task_id": _TYPE_STRING,
                    "project_id": _TYPE_STRING,
                    "process": _TYPE_STRING,
                    "window": _TYPE_STRING,
                    "keystrokes": _TYPE_NUMBER,
                    "mousemovements": _TYPE_NUMBER,
                    "deleted_by": _TYPE_STRING,
                    "deletedSeconds": _TYPE_NUMBER,
                }
            },
        }
        logs.log_json_obj("computer_activity.stdout", schema)
        logs.stdout_json_obj(schema)

    def write_records(user_id: str, user_name: str) -> None:
        """Write the records for this table."""

        def sass(obj: JSON, keys: List[str], default: Any) -> Any:
            """Safely get the nested value after accessing a dict."""
            obj = _get_nested_value(obj, keys)
            return default if obj is None else obj

        limit: int = 200
        offset: int = 0

        while True:
            (status_code, response) = api_worker.get_computer_activity(
                company_id,
                user_id,
                offset,
                Options(limit, options.start_date, adjusted_end_date),
            )
            ensure_200(status_code)

            response_obj: JSON = json.loads(response)

            logs.log_json_obj("computer_activity", response_obj)

            computer_activity = response_obj.get("data", [])
            paging = response_obj.get("paging", "")

            for record in computer_activity:
                project_id = record["numbers"][0]["meta"].get("projectId", "")

                stdout_json_obj: JSON = {
                    "type": "RECORD",
                    "stream": "computer_activity",
                    "record": {
                        "uuid": str(uuid.uuid4()),
                        "date": translate_date(record["date"]),
                        "user_id": user_id,
                        "user_name": standard_name(user_name),
                        "keystrokes": record["numbers"][0]["meta"]["keys"],
                        "mousemovements": record["numbers"][0]["meta"][
                            "movements"
                        ],
                        "project_id": project_dict.get(project_id, "Deleted"),
                    },
                }

                stdout_json_obj["record"]["task_id"] = sass(
                    record["numbers"][0], ["meta", "taskId"], "Deleted"
                )
                stdout_json_obj["record"]["process"] = sass(
                    record, ["appInfo", "process"], ""
                )
                stdout_json_obj["record"]["window"] = sass(
                    record, ["appInfo", "window"], ""
                )
                stdout_json_obj["record"]["deleted_by"] = sass(
                    record, ["deleted_by"], ""
                )
                stdout_json_obj["record"]["deletedSeconds"] = sass(
                    record, ["deletedSeconds"], 0.0
                )

                logs.log_json_obj("computer_activity.stdout", stdout_json_obj)
                logs.stdout_json_obj(stdout_json_obj)

            if paging.get("next", ""):
                offset = paging["next"]
            else:
                break

    write_schema()
    for user_id, user_name in users_list:
        write_records(user_id, user_name)


def main() -> None:  # pylint: disable=too-many-locals
    """Usual entry point."""

    # user interface
    def check_date(date: str) -> str:
        re_date = r"([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))"
        if not re.match(re_date, date):
            raise argparse.ArgumentTypeError(
                f"{date} does not have the correct format (yyyy-mm-dd)"
            )
        return date

    # by default all the data from a year ago is extracted
    today = datetime.date.today()
    start_date = today.replace(today.year - 1).isoformat()
    end_date = today.isoformat()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--start-date",
        type=check_date,
        required=False,
        default=start_date,
    )
    parser.add_argument(
        "-e", "--end-date", type=check_date, required=False, default=end_date
    )
    parser.add_argument("--work-logs", "-w", action="store_true")
    parser.add_argument("--computer-activity", "-ca", action="store_true")
    args = parser.parse_args()

    start_date = args.start_date or start_date
    end_date = args.end_date or end_date

    auth_data = {
        "email": os.environ["ANALYTICS_TIMEDOCTOR_USER"],
        "password": os.environ["ANALYTICS_TIMEDOCTOR_PASSWD"],
        "totpCode": "",
        "permissions": "read",
    }
    auth_bytes = json.dumps(auth_data).encode()
    auth_request = request.Request(
        "https://api2.timedoctor.com/api/1.0/login", data=auth_bytes
    )
    auth_request.add_header("Content-Type", "application/json")
    with request.urlopen(auth_request) as result:
        response = result.read().decode("utf-8")

    access_token: str = json.loads(response)["data"]["token"]
    api_worker = Worker(access_token)

    # get some account info by inspecting the admin account (the token owner)
    (status_code, response) = api_worker.get_companies()
    ensure_200(status_code)
    account_info: dict = json.loads(response)["data"]
    company_id = str(account_info["companies"][0]["id"])

    # get the id of all users in the company
    (status_code, response) = api_worker.get_users(company_id)
    ensure_200(status_code)
    users: List[List[str]] = [
        [user["id"], user["name"]] for user in json.loads(response)["data"]
    ]

    # get dict of project_ids with their project_names
    (status_code, response) = api_worker.get_projects(company_id)
    ensure_200(status_code)
    projects: Dict[str, str] = {
        project["id"]: project["name"]
        for project in json.loads(response)["data"]
    }

    # sync
    try:
        if args.work_logs:
            sync_worklogs(api_worker, company_id, users, start_date, end_date)
        if args.computer_activity:
            sync_computer_activity(
                api_worker,
                company_id,
                users,
                projects,
                Options(0, start_date, end_date),
            )
    finally:
        api_worker.logout()


if __name__ == "__main__":
    main()
