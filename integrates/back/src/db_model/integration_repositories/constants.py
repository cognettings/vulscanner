from db_model import (
    TABLE,
)
from dynamodb.types import (
    Facet,
)

GSI_2_FACET = Facet(
    attrs=TABLE.facets["organization_unreliable_integration_repository"].attrs,
    pk_alias="CRED#credential_id",
    sk_alias="URL#hash",
)
