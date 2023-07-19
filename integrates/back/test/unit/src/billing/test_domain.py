from back.test.unit.src.utils import (
    get_module_at_test,
    set_mocks_return_values,
)
from billing.domain import (
    customer_has_payment_method,
    customer_portal,
    get_customer,
    get_document_link,
    get_prices,
    list_customer_payment_methods,
)
from billing.types import (
    Customer,
    PaymentMethod,
    Price,
)
from custom_exceptions import (
    InvalidBillingCustomer,
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
from decimal import (
    Decimal,
)
import os
import pytest
from resources.domain import (
    remove_file,
    save_file,
    search_file,
)
from starlette.datastructures import (
    UploadFile,
)
from unittest.mock import (
    AsyncMock,
    patch,
)

MODULE_AT_TEST = get_module_at_test(file_path=__file__)

pytestmark = [
    pytest.mark.asyncio,
]


@patch(MODULE_AT_TEST + "dal.get_prices", new_callable=AsyncMock)
async def test_get_prices(mock_dal_get_prices: AsyncMock) -> None:
    price = Price(id="2334", currency="us", amount=100)
    mock_dal_get_prices.return_value = {"item": price}

    result = await get_prices()

    assert result == mock_dal_get_prices.return_value


@patch(MODULE_AT_TEST + "dal.create_customer", new_callable=AsyncMock)
@patch(MODULE_AT_TEST + "dal.get_customer_portal", new_callable=AsyncMock)
async def test_customer_portal(
    mock_dal_get_customer_portal: AsyncMock,
    mock_dal_create_customer: AsyncMock,
) -> None:
    mock_dal_get_customer_portal.return_value = "returned_string"

    mock_dal_create_customer.return_value = Customer(
        id="564",
        name="Charles",
        address=None,
        email="test@fluid.com",
        phone="5687867653",
        default_payment_method="cash",
    )

    org_id = "fluid132"
    org_name = "fluid_test_name"
    user_email = "fluid@test.com"

    result = await customer_portal(
        org_id=org_id,
        org_name=org_name,
        user_email=user_email,
        org_billing_customer=None,
    )

    assert result == mock_dal_get_customer_portal.return_value


@pytest.mark.parametrize(["org_billing_customer"], [["costumer_string"]])
@patch(MODULE_AT_TEST + "dal.get_customer", new_callable=AsyncMock)
async def test_customer_has_payment_method(
    mock_dal_get_costumer: AsyncMock, org_billing_customer: str
) -> None:
    mock_dal_get_costumer.return_value = Customer(
        id="56",
        name="Dorian",
        address=None,
        email="test@fluid.com",
        phone="5645567653",
        default_payment_method="cash",
    )

    result = await customer_has_payment_method(
        org_billing_customer=org_billing_customer
    )

    assert result is True


@pytest.mark.parametrize(["org_billing_customer"], [[None]])
async def test_get_customer_raises_exception(
    org_billing_customer: str,
) -> None:
    with pytest.raises(InvalidBillingCustomer):
        await get_customer(org_billing_customer=org_billing_customer)


@pytest.mark.parametrize(["org_billing_customer"], [["test"]])
@patch(MODULE_AT_TEST + "dal.get_customer", new_callable=AsyncMock)
async def test_get_customer(
    mock_dal_get_costumer: AsyncMock, org_billing_customer: str
) -> None:
    mock_dal_get_costumer.return_value = Customer(
        id="23323",
        name="peter",
        address=None,
        email="test@fluid.com",
        phone="3334567654",
        default_payment_method="cash",
    )

    result = await get_customer(org_billing_customer=org_billing_customer)

    assert result == mock_dal_get_costumer.return_value
    mock_dal_get_costumer.assert_called_once()


@pytest.mark.parametrize(
    ("organization", "expected_result"),
    (
        (
            Organization(
                created_by="unknown@unknown.com",
                created_date=datetime.fromisoformat(
                    "2018-02-08T00:43:18+00:00"
                ),
                id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="okada",
                policies=Policies(
                    modified_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    modified_by="integratesmanager@gmail.com",
                    inactivity_period=90,
                    max_acceptance_days=60,
                    max_acceptance_severity=Decimal("10.0"),
                    max_number_acceptances=2,
                    min_acceptance_severity=Decimal("0.0"),
                    min_breaking_severity=Decimal("0"),
                    vulnerability_grace_period=0,
                ),
                state=OrganizationState(
                    status=OrganizationStateStatus.ACTIVE,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat(
                        "2018-02-08T00:43:18+00:00"
                    ),
                    pending_deletion_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
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
                        documents=OrganizationDocuments(rut=None, tax_id=None),
                    ),
                    OrganizationPaymentMethods(
                        id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                        business_name="Testing Company and Sons",
                        email="test@fluidattacks.com",
                        country="Colombia",
                        state="Antioquia",
                        city="Medellín",
                        documents=OrganizationDocuments(rut=None, tax_id=None),
                    ),
                ],
                billing_customer=None,
                vulnerabilities_url=None,
            ),
            [
                PaymentMethod(
                    id="38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                    fingerprint="",
                    last_four_digits="",
                    expiration_month="",
                    expiration_year="",
                    brand="",
                    default=False,
                    business_name="Fluid",
                    city="Medellín",
                    country="Colombia",
                    email="test@fluidattacks.com",
                    state="Antioquia",
                    rut=None,
                    tax_id=None,
                ),
                PaymentMethod(
                    id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                    fingerprint="",
                    last_four_digits="",
                    expiration_month="",
                    expiration_year="",
                    brand="",
                    default=False,
                    business_name="Testing Company and Sons",
                    city="Medellín",
                    country="Colombia",
                    email="test@fluidattacks.com",
                    state="Antioquia",
                    rut=None,
                    tax_id=None,
                ),
            ],
        ),
    ),
)
async def test_customer_payment_methods(
    organization: Organization, expected_result: list
) -> None:
    result = await list_customer_payment_methods(org=organization)
    assert result == expected_result


@pytest.mark.parametrize(
    ("organization", "payment_id", "file_name", "expected_result"),
    (
        (
            Organization(
                created_by="unknown@unknown.com",
                created_date=datetime.fromisoformat(
                    "2018-02-08T00:43:18+00:00"
                ),
                id="ORG#38eb8f25-7945-4173-ab6e-0af4ad8b7ef3",
                name="okada",
                policies=Policies(
                    modified_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
                    modified_by="integratesmanager@gmail.com",
                    inactivity_period=90,
                    max_acceptance_days=60,
                    max_acceptance_severity=Decimal("10.0"),
                    max_number_acceptances=2,
                    min_acceptance_severity=Decimal("0.0"),
                    min_breaking_severity=Decimal("0"),
                    vulnerability_grace_period=0,
                ),
                state=OrganizationState(
                    status=OrganizationStateStatus.ACTIVE,
                    modified_by="unknown",
                    modified_date=datetime.fromisoformat(
                        "2018-02-08T00:43:18+00:00"
                    ),
                    pending_deletion_date=datetime.fromisoformat(
                        "2019-11-22T20:07:57+00:00"
                    ),
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
                        documents=OrganizationDocuments(rut=None, tax_id=None),
                    ),
                    OrganizationPaymentMethods(
                        id="4722b0b7-cfeb-4898-8308-185dfc2523bc",
                        business_name="Testing Company and Sons",
                        email="test@fluidattacks.com",
                        country="Colombia",
                        state="Antioquia",
                        city="Medellín",
                        documents=OrganizationDocuments(rut=None, tax_id=None),
                    ),
                ],
                billing_customer=None,
                vulnerabilities_url=None,
            ),
            "4722b0b7-cfeb-4898-8308-185dfc2523bc",
            "test_file.pdf",
            "https://s3.amazonaws.com/integrates/johndoeatfluid-test-unit/"
            "resources/billing/okada/testing%20company%20and%20sons/"
            "test_file.pdf?X-Amz-Algorithm=TestX-Amz-Credential=Testus-east-1"
            "%2Fs3%2Faws4_request&X-Amz-Date=20230117T170631Z&X-Amz-Expires=10"
            "&X-Amz-SignedHeaders=host&X-Amz-Security-Token=TestX-Amz-"
            "Signature=Test",
        ),
    ),
)
@patch(MODULE_AT_TEST + "s3_ops.sign_url", new_callable=AsyncMock)
async def test_get_document_link(
    mock_s3_ops_sign_url: AsyncMock,
    organization: Organization,
    payment_id: str,
    file_name: str,
    expected_result: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[organization.name, payment_id, file_name]],
        mocked_objects=[mock_s3_ops_sign_url],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.sign_url"],
    )
    result = await get_document_link(organization, payment_id, file_name)
    assert mock_s3_ops_sign_url.called is True
    assert result == expected_result


@pytest.mark.parametrize(
    ["file_name", "content_type"],
    [
        ["billing-test-file.png", "image/png"],
        ["unittesting-test-file.csv", "text/csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.upload_memory_file", new_callable=AsyncMock)
async def test_save_file(
    mock_s3_ops_upload_memory_file: AsyncMock,
    file_name: str,
    content_type: str,
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_upload_memory_file],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.upload_memory_file"],
    )

    file_location = os.path.dirname(os.path.abspath(__file__))
    file_location = os.path.join(file_location, "mock/resources/" + file_name)
    with open(file_location, "rb") as data:
        test_file = UploadFile(data.name, data, content_type)
        await save_file(file_object=test_file, file_name=file_name)
    mock_s3_ops_upload_memory_file.assert_called_with(
        test_file, f"resources/{file_name}"
    )


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.list_files", new_callable=AsyncMock)
async def test_search_file(
    mock_s3_ops_list_files: AsyncMock, file_name: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_list_files],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.list_files"],
    )

    assert file_name in await search_file(file_name)
    mock_s3_ops_list_files.assert_called_with(f"resources/{file_name}")


@pytest.mark.parametrize(
    ["file_name"],
    [
        ["billing-test-file.png"],
        ["unittesting-test-file.csv"],
    ],
)
@patch(MODULE_AT_TEST + "s3_ops.remove_file", new_callable=AsyncMock)
async def test_remove_file(
    mock_s3_ops_remove_file: AsyncMock, file_name: str
) -> None:
    assert set_mocks_return_values(
        mocks_args=[[file_name]],
        mocked_objects=[mock_s3_ops_remove_file],
        module_at_test=MODULE_AT_TEST,
        paths_list=["s3_ops.remove_file"],
    )

    await remove_file(file_name)
    mock_s3_ops_remove_file.assert_called_with(f"resources/{file_name}")
