from dynamodb.types import (
    Facet,
    PrimaryKey,
    Table,
)
from s3.model.types import (
    Advisory,
)

TABLE = Table(
    name="test_table",
    primary_key=PrimaryKey(partition_key="pk", sort_key="sk"),
    facets={
        "advisories": Facet(
            attrs=(
                "associated_advisory",
                "cwe_ids",
                "package_name",
                "package_manager",
                "vulnerable_version",
                "severity",
                "source",
                "created_at",
                "modified_at",
            ),
            pk_alias="PLATFORM#platform#PACKAGE#pkg_name",
            sk_alias="SOURCE#src#ADVISORY#id",
        )
    },
    indexes={},
)
PRIMARY_KEY_TEST = PrimaryKey("pk_value", "sk_value")
STR_PKG_ADVISORIES: str = "db_model.advisories"
STR_MDL_ADD: str = f"{STR_PKG_ADVISORIES}.add"
STR_MDL_UPDATE: str = f"{STR_PKG_ADVISORIES}.update"
STR_MDL_REMOVE: str = f"{STR_PKG_ADVISORIES}.remove"
ADVISORY_TEST = Advisory(
    id="ADV-123",
    package_name="test_package",
    package_manager="test_manager",
    vulnerable_version="1.0.0",
    source="test_source",
    cwe_ids=["CWE-123"],
    severity="high",
)
