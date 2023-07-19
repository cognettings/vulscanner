# pylint: disable=too-many-locals

from billing import (
    domain as billing_domain,
)
from custom_exceptions import (
    InvalidFileSize,
    InvalidFileType,
)
from custom_utils import (
    datetime as datetime_utils,
    files as files_utils,
    validations_deco,
)
from db_model.organizations.types import (
    DocumentFile,
    Organization,
    OrganizationDocuments,
)
from resources import (
    domain as resources_domain,
)
from starlette.datastructures import (
    UploadFile,
)


@validations_deco.validate_file_name_deco("file.filename")
@validations_deco.validate_fields_deco(["file.content_type"])
@validations_deco.validate_sanitized_csv_input_deco(
    ["file.filename", "file.content_type"]
)
async def validate_file(file: UploadFile) -> None:
    mib = 1048576
    allowed_mimes = [
        "image/gif",
        "image/jpeg",
        "image/png",
        "application/pdf",
    ]
    if not await files_utils.assert_uploaded_file_mime(file, allowed_mimes):
        raise InvalidFileType("TAX_ID")

    if await files_utils.get_file_size(file) > 10 * mib:
        raise InvalidFileSize()


async def validate_legal_document(
    rut: UploadFile | None, tax_id: UploadFile | None
) -> None:
    if rut:
        await validate_file(file=rut)
    if tax_id:
        await validate_file(file=tax_id)


def document_extension(document: UploadFile) -> str:
    extension = {
        "image/gif": ".gif",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/pdf": ".pdf",
        "application/zip": ".zip",
        "text/csv": ".csv",
        "text/plain": ".txt",
    }.get(document.content_type, "")

    return extension


@validations_deco.validate_length_deco("business_name", max_length=60)
@validations_deco.validate_fields_deco(["business_name", "email"])
async def update_documents(
    *,
    org: Organization,
    payment_method_id: str,
    business_name: str,
    city: str,
    country: str,
    email: str,
    state: str,
    rut: UploadFile | None = None,
    tax_id: UploadFile | None = None,
) -> bool:
    documents = OrganizationDocuments()
    org_name = org.name.lower()
    business_name = business_name.lower()

    if org.payment_methods:
        actual_payment_method = list(
            filter(
                lambda method: method.id == payment_method_id,
                org.payment_methods,
            )
        )[0]
        if actual_payment_method.business_name.lower() != business_name:
            document_prefix = (
                f"billing/{org.name.lower()}/"
                + f"{actual_payment_method.business_name.lower()}"
            )
            file_name: str = ""
            if actual_payment_method.documents.rut:
                file_name = actual_payment_method.documents.rut.file_name
            if actual_payment_method.documents.tax_id:
                file_name = actual_payment_method.documents.tax_id.file_name

            await resources_domain.remove_file(
                f"{document_prefix}/{file_name}"
            )

    if rut:
        rut_file_name = f"{org_name}-{business_name}{document_extension(rut)}"
        rut_full_name = f"billing/{org_name}/{business_name}/{rut_file_name}"
        await resources_domain.save_file(
            file_object=rut, file_name=rut_full_name
        )
        documents = OrganizationDocuments(
            rut=DocumentFile(
                file_name=rut_file_name,
                modified_date=datetime_utils.get_utc_now(),
            )
        )
    if tax_id:
        tax_id_file_name = (
            f"{org_name}-{business_name}{document_extension(tax_id)}"
        )
        tax_id_full_name = (
            f"billing/{org_name}/{business_name}/{tax_id_file_name}"
        )
        await resources_domain.save_file(
            file_object=tax_id, file_name=tax_id_full_name
        )
        documents = OrganizationDocuments(
            tax_id=DocumentFile(
                file_name=tax_id_file_name,
                modified_date=datetime_utils.get_utc_now(),
            )
        )

    return await billing_domain.update_other_payment_method(
        org=org,
        documents=documents,
        payment_method_id=payment_method_id,
        business_name=business_name,
        city=city,
        country=country,
        email=email,
        state=state,
    )
