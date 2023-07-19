# pylint: disable=import-error
from back.test import (
    db,
)
from datetime import (
    datetime,
)
from db_model.organizations.enums import (
    OrganizationStateStatus,
)
from db_model.organizations.types import (
    Organization,
    OrganizationDocuments,
    OrganizationPaymentMethods,
    OrganizationState,
)
from db_model.types import (
    Policies,
)
import pytest
import pytest_asyncio
from typing import (
    Any,
)


@pytest.mark.resolver_test_group("update_other_payment_method")
@pytest_asyncio.fixture(autouse=True, scope="session")
async def populate(generic_data: dict[str, Any]) -> bool:
    data: dict[str, Any] = {
        "organizations": [
            {
                "organization": Organization(
                    created_by=generic_data["global_vars"]["user_email"],
                    created_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    country="Colombia",
                    payment_methods=[
                        OrganizationPaymentMethods(
                            id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                            business_name="Fluid",
                            email="test@fluidattacks.com",
                            country="Colombia",
                            state="Antioquia",
                            city="Medellín",
                            documents=OrganizationDocuments(
                                rut=None, tax_id=None
                            ),
                        ),
                        OrganizationPaymentMethods(
                            id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                            business_name="Testing Company and Sons",
                            email="test@fluidattacks.com",
                            country="Colombia",
                            state="Antioquia",
                            city="Medellín",
                            documents=OrganizationDocuments(
                                rut=None, tax_id=None
                            ),
                        ),
                    ],
                    id="40f6da5f-4f66-4bf0-825b-a2d9748ad6db",
                    name="orgtest",
                    policies=Policies(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                    ),
                    state=OrganizationState(
                        modified_by=generic_data["global_vars"]["user_email"],
                        modified_date=datetime.fromisoformat(
                            "2019-11-22T20:07:57+00:00"
                        ),
                        status=OrganizationStateStatus.ACTIVE,
                    ),
                ),
            },
        ],
        "policies": [
            {
                "level": "user",
                "subject": "test@fluidattacks.com",
                "object": "self",
                "role": "admin",
            },
        ],
    }
    return await db.populate({**generic_data["db_data"], **data})
