from .utils import (
    format_indicators,
    format_to_expression_attributes_names,
    format_to_expression_attributes_values,
    format_to_project_expression,
    format_to_update_expression,
    LOGGER,
)
from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from botocore.exceptions import (
    ClientError,
)
from dynamodb.resource import (
    TABLE_RESOURCE,
)
from dynamodb.types import (
    Item,
)


def get_finding(
    *,
    pk: str,
    sk: str,
) -> Item:
    """using exact pk and sk, returns the finding item
    from dynamodb.
    """
    args = set(
        [
            "pk",
            "sk",
            "state",
            "unreliable_indicators",
            "group_name",
            "severity_score",
        ]
    )
    query_args = {
        "ExpressionAttributeNames": format_to_expression_attributes_names(
            args
        ),
        "Key": {
            "pk": pk,
            "sk": sk,
        },
        "ProjectionExpression": format_to_project_expression(args),
    }
    response = TABLE_RESOURCE.get_item(**query_args)
    item: Item = response.get("Item", {})
    return item


def get_vulnerabilities_by_finding(
    *,
    finding_id: str,
) -> list[Item]:
    """using exact finding_id, returns vulnerabilities
    in finding from dynamodb.
    """
    args = set(
        [
            "pk",
            "sk",
            "created_date",
            "group_name",
            "state",
            "treatment",
            "zero_risk",
            "severity_score",
            "unreliable_indicators",
        ]
    )
    query_args = {
        "ExpressionAttributeNames": format_to_expression_attributes_names(
            args
        ),
        "IndexName": "inverted_index",
        "KeyConditionExpression": (
            Key("sk").eq(finding_id) & Key("pk").begins_with("VULN#")
        ),
        "ProjectionExpression": format_to_project_expression(args),
        "Limit": 100,
    }

    response = TABLE_RESOURCE.query(**query_args)
    items: list[Item] = response.get("Items", [])
    return items


def get_released_nzr_vulns_by_finding(
    *,
    finding_id: str,
) -> list[Item]:
    """Filter the released and non-zero risk
    vulnerabilities by `finding_id`.

    Released vulnerabilities have `SAFE` and `VULNERABLE` status
    (these are displayed to the user).

    Non-zero risk vulnerabilities are those that they are safe
    or they are vulnerable with zero risk status, but
    they are not `CONFIRMED` or `REQUESTED` for zero risk.
    """
    vulns = get_vulnerabilities_by_finding(
        finding_id=finding_id,
    )
    released_vulns = [
        vuln
        for vuln in vulns
        if vuln["state"]["status"] in ["SAFE", "VULNERABLE"]
    ]
    nzr_vulns = [
        vuln
        for vuln in released_vulns
        if not (
            "zero_risk" in vuln
            and vuln["zero_risk"]["status"] in ["CONFIRMED", "REQUESTED"]
        )
    ]
    return nzr_vulns


def update_indicators(
    *,
    finding: Item | None,
    current_indicators: Item,
    new_indicators: Item,
) -> None:
    if not finding:
        return

    pk_value = finding["pk"]
    sk_value = finding["sk"]
    current_indicators = format_indicators(current_indicators)
    new_indicators = format_indicators(new_indicators)

    # Optimistic locking to prevent overwriting
    # if something else changed it first.
    condition_expression = Attr("pk").exists()
    for key in new_indicators.keys():
        if key in current_indicators:
            condition_expression &= Attr(key).eq(current_indicators[key])

    try:
        TABLE_RESOURCE.update_item(
            ConditionExpression=condition_expression,
            ExpressionAttributeValues=format_to_expression_attributes_values(
                new_indicators
            ),
            Key={"pk": pk_value, "sk": sk_value},
            UpdateExpression=format_to_update_expression(new_indicators),
        )
        LOGGER.info("pk: %s, sk: %s", pk_value, sk_value)
        LOGGER.info(new_indicators)
        LOGGER.info("Done!\n")
    except ClientError as ex:
        if ex.response["Error"]["Code"] == "ConditionalCheckFailedException":
            LOGGER.info("Optimistic locking error for %s", pk_value)
        else:
            raise
