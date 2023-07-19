from arch_lint.dag import (
    DAG,
)
from pathlib import (
    Path,
)
from typing import (
    cast,
)

_dag: tuple[frozenset[str], ...] = (
    frozenset({"cli"}),
    frozenset({"app"}),
    frozenset({"schedulers"}),
    frozenset({"api"}),
    frozenset({"server_async"}),
    frozenset({"batch_dispatch"}),
    frozenset({"search"}),
    frozenset({"remove_stakeholder"}),
    frozenset({"unreliable_indicators"}),
    frozenset({"outside_repositories"}),
    frozenset({"billing"}),
    frozenset({"forces"}),
    frozenset({"reports"}),
    frozenset({"toe"}),
    frozenset({"groups"}),
    frozenset({"group_comments"}),
    frozenset({"events"}),
    frozenset({"vulnerability_files"}),
    frozenset({"findings"}),
    frozenset({"machine"}),
    frozenset({"organizations_finding_policies"}),
    frozenset({"vulnerabilities"}),
    frozenset({"roots"}),
    frozenset({"oauth"}),
    frozenset({"notifications"}),
    frozenset({"event_comments"}),
    frozenset({"finding_comments"}),
    frozenset({"analytics"}),
    frozenset({"tags"}),
    frozenset({"organizations"}),
    frozenset({"stakeholders"}),
    frozenset({"decorators"}),
    frozenset({"mailer"}),
    frozenset({"organization_access"}),
    frozenset({"group_access"}),
    frozenset({"authz"}),
    frozenset({"batch"}),
    frozenset({"trials"}),
    frozenset({"resources"}),
    frozenset({"custom_utils"}),
    frozenset({"sessions"}),
    frozenset({"dataloaders"}),
    frozenset({"db_model"}),
    frozenset({"dynamodb"}),
    frozenset({"s3"}),
    frozenset({"sqs"}),
    frozenset({"verify"}),
    frozenset({"settings"}),
    frozenset({"sms"}),
    frozenset({"custom_exceptions"}),
    frozenset({"telemetry"}),
    frozenset({"context"}),
    frozenset({"class_types"}),
)


def project_dag() -> DAG:
    return cast(DAG, DAG.new(_dag))


def empty_folder_filter(path: Path) -> bool:
    return path.is_file() or any(child.is_file() for child in path.iterdir())
