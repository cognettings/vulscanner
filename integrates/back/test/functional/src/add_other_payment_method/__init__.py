# pylint: disable=import-error
from back.test.functional.src.utils import (
    get_graphql_result,
)
from dataloaders import (
    get_new_context,
)
import os
from starlette.datastructures import (
    UploadFile,
)


async def get_result(
    *,
    user: str,
    organization_id: str,
    business_name: str,
    email: str,
    country: str,
    state: str,
    city: str,
    # should_use_invalid: bool = False,
) -> dict:
    query: str = """
        mutation addOtherPaymentMethod($organizationId: String!,
            $businessName: String!,
            $email: String!,
            $country: String!,
            $state: String!,
            $city: String!,
            $rut: Upload,
            $taxId: Upload,
            ) {
                addOtherPaymentMethod(
                    organizationId: $organizationId
                    businessName: $businessName
                    email: $email
                    country: $country
                    state: $state
                    city: $city
                    rut: $rut
                    taxId: $taxId
                ) {
                    success
            }
        }
    """
    filename: str
    uploaded_file: UploadFile
    variables: dict
    data: dict
    result: dict
    path: str = os.path.dirname(os.path.abspath(__file__))

    filename = f"{path}/test-pdf.pdf"
    with open(filename, "rb") as test_file:
        uploaded_file = UploadFile(
            "orgtest-group1-0123456789.pdf", test_file, "application/pdf"
        )
        variables = {
            "organizationId": organization_id,
            "businessName": business_name,
            "email": email,
            "country": country,
            "state": state,
            "city": city,
            "rut": uploaded_file,
            "taxId": None,
        }
        data = {"query": query, "variables": variables}
        result = await get_graphql_result(
            data,
            stakeholder=user,
            context=get_new_context(),
        )

    return result
