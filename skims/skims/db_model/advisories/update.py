from .utils import (
    format_advisory,
    print_exc,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    AdvisoryDoesNotExist,
    AdvisoryNotModified,
    InvalidSeverity,
    InvalidVulnerableVersion,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    keys,
    operations,
)
from dynamodb.types import (
    PrimaryKey,
)
from s3.model.types import (
    Advisory,
)

ACTION = "updated"


async def update(
    *,
    advisory: Advisory,
    checked: bool = False,
    to_storage: list[Advisory] | None = None,
) -> None:
    try:
        await _update(advisory=advisory, checked=checked)
        if to_storage is not None:
            to_storage.append(advisory)
    except (InvalidVulnerableVersion,) as exc:
        print_exc(exc, ACTION, advisory, f" ({advisory.vulnerable_version})")
    except (InvalidSeverity,) as exc:
        print_exc(exc, ACTION, advisory, f" ({advisory.severity})")
    except (
        AdvisoryDoesNotExist,
        AdvisoryNotModified,
    ) as exc:
        print_exc(exc, ACTION, advisory)


async def _check_update(
    *,
    advisory: Advisory,
    advisory_key: PrimaryKey,
) -> Advisory:
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(advisory_key.partition_key)
            & Key(key_structure.sort_key).eq(advisory_key.sort_key)
        ),
        facets=(TABLE.facets["advisories"],),
        limit=1,
        table=TABLE,
    )
    if not response.items:
        raise AdvisoryDoesNotExist()

    current_ad = response.items[0]
    if (
        current_ad.get("vulnerable_version") == advisory.vulnerable_version
        and current_ad.get("severity") == advisory.severity
        and current_ad.get("cwe_ids") == advisory.cwe_ids
    ):
        raise AdvisoryNotModified()
    return advisory._replace(created_at=current_ad.get("created_at"))


async def _update(
    *,
    advisory: Advisory,
    checked: bool,
) -> None:
    advisory = format_advisory(
        advisory=advisory, is_update=True, checked=checked
    )
    advisory_key = keys.build_key(
        facet=TABLE.facets["advisories"],
        values={
            "platform": advisory.package_manager,
            "pkg_name": advisory.package_name,
            "src": advisory.source,
            "id": advisory.id,
        },
    )
    if not checked:
        advisory = await _check_update(
            advisory=advisory, advisory_key=advisory_key
        )
    advisory_item = advisory._asdict()
    await operations.update_item(
        item=advisory_item,
        key=advisory_key,
        table=TABLE,
    )
    print(f"Updated ( {advisory_key.partition_key} {advisory_key.sort_key} )")
