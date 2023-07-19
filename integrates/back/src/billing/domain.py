from aioextensions import (
    collect,
)
from billing import (
    dal,
    utils as billing_utils,
)
from billing.subscriptions import (
    utils as subs_utils,
)
from billing.types import (
    Customer,
    PaymentMethod,
    Price,
    Subscription,
)
from context import (
    FI_MAIL_FINANCE,
)
from custom_exceptions import (
    BillingCustomerHasActiveSubscription,
    CouldNotCreatePaymentMethod,
    InvalidBillingCustomer,
    InvalidBillingPaymentMethod,
    InvalidExpiryDateField,
    PaymentMethodAlreadyExists,
)
from custom_utils import (
    datetime as datetime_utils,
    validations_deco,
)
from dataloaders import (
    get_new_context,
)
from db_model import (
    organizations as organizations_model,
)
from db_model.groups.enums import (
    GroupTier,
)
from db_model.organizations.types import (
    DocumentFile,
    Organization,
    OrganizationDocuments,
    OrganizationMetadataToUpdate,
    OrganizationPaymentMethods,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from mailer.common import (
    GENERAL_TAG,
    send_mails_async,
)
from notifications import (
    domain as notifications_domain,
)
from resources import (
    domain as resources_domain,
)
from s3 import (
    operations as s3_ops,
)
from settings import (
    LOGGING,
)
from starlette.datastructures import (
    UploadFile,
)
from starlette.requests import (
    Request,
)
from starlette.responses import (
    JSONResponse,
)
from stripe.error import (
    CardError,
    SignatureVerificationError,
)
from typing import (
    Any,
    cast,
)
import uuid

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)


async def get_document_link(
    org: Organization, payment_id: str, file_name: str
) -> str:
    org_name = org.name.lower()
    payment_method: list[OrganizationPaymentMethods] = []
    file_url = ""
    if org.payment_methods:
        payment_method = list(
            filter(lambda method: method.id == payment_id, org.payment_methods)
        )
        if len(payment_method) == 0:
            raise InvalidBillingPaymentMethod()
        business_name = payment_method[0].business_name.lower()
        file_url = f"billing/{org_name}/{business_name}/{file_name}"

    return await s3_ops.sign_url(
        f"resources/{file_url}",
        10,
    )


async def customer_has_payment_method(
    *,
    org_billing_customer: str,
) -> bool:
    customer: Customer = await dal.get_customer(
        org_billing_customer=org_billing_customer,
    )
    return customer.default_payment_method is not None


async def get_customer(
    *,
    org_billing_customer: str,
) -> Customer:
    # Raise exception if stripe customer does not exist
    if org_billing_customer is None:
        raise InvalidBillingCustomer()

    return await dal.get_customer(
        org_billing_customer=org_billing_customer,
    )


async def list_customer_payment_methods(
    *,
    org_billing_customer: Customer | None = None,
    org: Organization,
    limit: int = 100,
) -> list[PaymentMethod]:
    """Return list of customer's payment methods"""
    # Return empty list if stripe customer does not exist
    payment_methods = []

    if org.billing_customer is not None:
        customer = (
            org_billing_customer
            if org_billing_customer
            else await dal.get_customer(
                org_billing_customer=org.billing_customer,
            )
        )
        stripe_payment_methods: list[
            dict[str, Any]
        ] = await dal.get_customer_payment_methods(
            org_billing_customer=customer.id,
            limit=limit,
        )

        payment_methods += [
            PaymentMethod(
                id=payment_method["id"],
                fingerprint=payment_method["card"]["fingerprint"],
                last_four_digits=payment_method["card"]["last4"],
                expiration_month=str(payment_method["card"]["exp_month"]),
                expiration_year=str(payment_method["card"]["exp_year"]),
                brand=payment_method["card"]["brand"],
                default=payment_method["id"]
                == customer.default_payment_method,
                business_name="",
                city="",
                country="",
                email="",
                state="",
                rut=None,
                tax_id=None,
            )
            for payment_method in stripe_payment_methods
        ]

    if org.payment_methods is not None:
        other_payment_methods: list[
            OrganizationPaymentMethods
        ] = org.payment_methods

        payment_methods += [
            PaymentMethod(
                id=other_method.id,
                fingerprint="",
                last_four_digits="",
                expiration_month="",
                expiration_year="",
                brand="",
                default=False,
                business_name=other_method.business_name,
                city=other_method.city,
                country=other_method.country,
                email=other_method.email,
                state=other_method.state,
                rut=DocumentFile(
                    file_name=other_method.documents.rut.file_name,
                    modified_date=other_method.documents.rut.modified_date,
                )
                if other_method.documents.rut
                else None,
                tax_id=DocumentFile(
                    file_name=other_method.documents.tax_id.file_name,
                    modified_date=other_method.documents.tax_id.modified_date,
                )
                if other_method.documents.tax_id
                else None,
            )
            for other_method in other_payment_methods
        ]

    return payment_methods


async def customer_portal(
    *,
    org_id: str,
    org_name: str,
    user_email: str,
    org_billing_customer: str | None,
) -> str:
    """Create Stripe portal session"""
    # Create customer if it does not exist
    if org_billing_customer is None:
        customer: Customer = await dal.create_customer(
            org_id=org_id,
            org_name=org_name,
            user_email=user_email,
        )
        org_billing_customer = customer.id

    return await dal.get_customer_portal(
        org_billing_customer=org_billing_customer,
        org_name=org_name,
    )


async def create_billing_customer(
    org: Organization,
    user_email: str,
) -> Customer:
    customer: Customer | None = None
    billing_customer = org.billing_customer
    if billing_customer is None:
        customer = await dal.create_customer(
            org_id=org.id,
            org_name=org.name,
            user_email=user_email,
        )
    else:
        customer = await dal.get_customer(
            org_billing_customer=billing_customer,
        )

    return customer


async def create_credit_card_payment_method(
    *,
    org: Organization,
    user_email: str,
    make_default: bool,
    payment_method_id: str,
) -> bool:
    """Create a credit card payment method and associate it to the customer"""

    # Create customer if it does not exist
    customer = await create_billing_customer(org, user_email)

    result: bool = False
    results = await collect(
        [
            list_customer_payment_methods(
                org_billing_customer=customer, org=org, limit=1000
            ),
            dal.retrieve_payment_method(
                default=make_default,
                payment_method_id=payment_method_id,
            ),
        ]
    )

    # Raise exception if payment method already exists for customer
    payment_methods = cast(list[PaymentMethod], results[0])
    new_payment_method = cast(PaymentMethod, results[1])
    if new_payment_method.fingerprint in (
        payment_method.fingerprint for payment_method in payment_methods
    ):
        raise PaymentMethodAlreadyExists()

    # Attach payment method to customer
    try:
        result = await dal.attach_payment_method(
            payment_method_id=payment_method_id,
            org_billing_customer=customer.id,
        )
        await send_mails_async(
            loaders=get_new_context(),
            email_to=[FI_MAIL_FINANCE],
            context={
                "date": datetime_utils.get_as_str(
                    datetime_utils.get_now(), "%Y-%m-%d %H:%M:%S %Z"
                ),
                "last_digits": new_payment_method.last_four_digits,
                "organization": org.name,
                "responsible": user_email,
            },
            subject="Fluid Attacks | New payment method added in "
            + f"[{org.name}]",
            tags=GENERAL_TAG,
            template_name="credit_card_added",
        )
    except CardError as ex:
        raise CouldNotCreatePaymentMethod() from ex

    # If payment method is the first one registered or selected as default,
    # then make it default
    if not customer.default_payment_method or make_default:
        await dal.update_default_payment_method(
            payment_method_id=payment_method_id,
            org_billing_customer=customer.id,
        )

    return result


@validations_deco.validate_length_deco("business_name", max_length=60)
@validations_deco.validate_fields_deco(["business_name"])
async def create_other_payment_method(
    *,
    org: Organization,
    user_email: str,
    business_name: str,
    city: str,
    country: str,
    email: str,
    state: str,
    rut: UploadFile | None = None,
    tax_id: UploadFile | None = None,
) -> bool:
    """Create other payment method and associate it to the organization"""
    await billing_utils.validate_legal_document(rut, tax_id)

    other_payment_id = str(uuid.uuid4())
    other_payment = OrganizationPaymentMethods(
        business_name=business_name,
        city=city,
        country=country,
        documents=OrganizationDocuments(),
        email=email,
        id=other_payment_id,
        state=state,
    )

    # Raise exception if payment method already exists for organization
    if org.payment_methods:
        if business_name in (
            payment_method.business_name
            for payment_method in org.payment_methods
        ):
            raise PaymentMethodAlreadyExists()
        org.payment_methods.append(other_payment)
    else:
        org = org._replace(
            payment_methods=[other_payment],
        )
    await organizations_model.update_metadata(
        metadata=OrganizationMetadataToUpdate(
            payment_methods=org.payment_methods
        ),
        organization_id=org.id,
        organization_name=org.name,
    )
    await notifications_domain.request_other_payment_methods(
        business_legal_name=business_name,
        city=city,
        country=country,
        efactura_email=email,
        rut=rut,
        tax_id=tax_id,
        user_email=user_email,
    )
    return await billing_utils.update_documents(
        org=org,
        payment_method_id=other_payment_id,
        business_name=business_name,
        city=city,
        country=country,
        email=email,
        state=state,
        rut=rut,
        tax_id=tax_id,
    )


async def update_credit_card_payment_method(
    *,
    org: Organization,
    payment_method_id: str,
    card_expiration_month: int,
    card_expiration_year: int,
    make_default: bool,
) -> bool:
    if not isinstance(card_expiration_month, int) and not isinstance(
        card_expiration_year, int
    ):
        raise InvalidExpiryDateField()

    # Raise exception if stripe customer does not exist
    if org.billing_customer is None:
        raise InvalidBillingCustomer()

    # Raise exception if payment method does not belong to organization
    payment_methods: list[PaymentMethod] = await list_customer_payment_methods(
        org=org,
        limit=1000,
    )
    if payment_method_id not in (
        payment_method.id for payment_method in list(payment_methods)
    ):
        raise InvalidBillingPaymentMethod()

    result: bool = await dal.update_payment_method(
        payment_method_id=payment_method_id,
        card_expiration_month=card_expiration_month,
        card_expiration_year=card_expiration_year,
    )
    if make_default:
        result = result and await dal.update_default_payment_method(
            payment_method_id=payment_method_id,
            org_billing_customer=org.billing_customer,
        )

    return result


@validations_deco.validate_length_deco("business_name", max_length=60)
@validations_deco.validate_fields_deco(["business_name"])
async def update_other_payment_method(
    *,
    org: Organization,
    documents: OrganizationDocuments,
    payment_method_id: str,
    business_name: str,
    city: str,
    country: str,
    email: str,
    state: str,
) -> bool:
    # Raise exception if payment method does not belong to organization
    payment_methods: list[PaymentMethod] = await list_customer_payment_methods(
        org=org,
        limit=1000,
    )
    if payment_method_id not in (
        payment_method.id for payment_method in list(payment_methods)
    ):
        raise InvalidBillingPaymentMethod()

    # get actual payment methods
    other_payment_methods: list[OrganizationPaymentMethods] = []
    if org.payment_methods:
        other_payment_methods = org.payment_methods

    other_payment_methods = list(
        filter(
            lambda method: method.id != payment_method_id,
            other_payment_methods,
        )
    )
    other_payment_methods.append(
        OrganizationPaymentMethods(
            business_name=business_name,
            city=city,
            country=country,
            documents=documents,
            email=email,
            id=payment_method_id,
            state=state,
        )
    )
    await organizations_model.update_metadata(
        metadata=OrganizationMetadataToUpdate(
            payment_methods=other_payment_methods
        ),
        organization_id=org.id,
        organization_name=org.name,
    )
    return True


async def _set_default_payment(
    payment_methods: list[PaymentMethod],
    payment_method_id: str,
    org: Organization,
) -> bool:
    # Set another payment method as default
    # if current credit card default will be deleted
    result: bool = True
    default: PaymentMethod = [
        payment_method
        for payment_method in payment_methods
        if payment_method.default
    ][0]
    credit_card_payment_methods = [
        credit_card_payment
        for credit_card_payment in payment_methods
        if credit_card_payment.last_four_digits
    ]
    if (
        len(credit_card_payment_methods) > 1
        and payment_method_id == default.id
    ):
        non_defaults = [
            payment_method
            for payment_method in payment_methods
            if not payment_method.default
        ]

        result = await dal.update_default_payment_method(
            payment_method_id=non_defaults[0].id,
            org_billing_customer=org.billing_customer,
        )

    return result


async def remove_payment_method(
    *,
    org: Organization,
    payment_method_id: str,
) -> bool:
    # Raise exception if stripe customer does not exist
    if org.billing_customer is None:
        raise InvalidBillingCustomer()

    payment_methods: list[PaymentMethod] = await list_customer_payment_methods(
        org=org,
        limit=1000,
    )

    # Raise exception if payment method does not belong to organization
    if payment_method_id not in (
        payment_method.id for payment_method in payment_methods
    ):
        raise InvalidBillingPaymentMethod()

    if (
        list(
            filter(
                lambda method: method.id == payment_method_id, payment_methods
            )
        )[0].last_four_digits
        == ""
    ):
        # get actual payment methods
        other_payment_methods: list[OrganizationPaymentMethods] = []
        if org.payment_methods:
            other_payment_methods = org.payment_methods

        payment_method = list(
            filter(
                lambda method: method.id == payment_method_id,
                other_payment_methods,
            )
        )[0]
        business_name = payment_method.business_name
        other_payment_methods = list(
            filter(
                lambda method: method.id != payment_method_id,
                other_payment_methods,
            )
        )
        await organizations_model.update_metadata(
            metadata=OrganizationMetadataToUpdate(
                payment_methods=other_payment_methods
            ),
            organization_id=org.id,
            organization_name=org.name,
        )
        document_prefix = f"billing/{org.name.lower()}/{business_name.lower()}"
        file_name: str = ""
        if payment_method.documents.rut:
            file_name = payment_method.documents.rut.file_name
        if payment_method.documents.tax_id:
            file_name = payment_method.documents.tax_id.file_name

        await resources_domain.remove_file(f"{document_prefix}/{file_name}")

        return True

    subscriptions: list[Subscription] = await dal.get_customer_subscriptions(
        org_billing_customer=org.billing_customer,
        limit=1000,
        status="",
    )

    # Raise exception if payment method is the last one
    # and there are active or trialing subscriptions
    if len(payment_methods) == 1 and subs_utils.has_subscription(
        statuses=["active", "trialing"], subscriptions=subscriptions
    ):
        raise BillingCustomerHasActiveSubscription()

    update_default_payment = await _set_default_payment(
        payment_methods, payment_method_id, org
    )
    result = update_default_payment and await dal.remove_payment_method(
        payment_method_id=payment_method_id,
    )

    return result


async def get_prices() -> dict[str, Price]:
    """Get model prices"""
    return await dal.get_prices()


async def webhook(request: Request) -> JSONResponse:
    """Parse Stripe webhook request and execute event"""
    message: str = ""
    status: str = "success"

    try:
        # Create stripe webhook event
        event = await dal.create_webhook_event(
            request=request,
        )

        # Main logic
        tier: str = ""
        if event.type in (
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
        ):
            if event.data.object.status in ("active", "trialing"):
                tier = event.data.object.metadata.subscription
            elif event.data.object.status in ("canceled", "unpaid"):
                tier = "free"

        else:
            message = f"Unhandled event type: {event.type}"
            status = "failed"
            LOGGER.warning(message, extra=dict(extra=locals()))

        if tier != "":
            await groups_domain.update_group_tier(
                loaders=get_new_context(),
                comments=f"Triggered by Stripe with event {event.id}",
                group_name=str(event.data.object.metadata.group).lower(),
                tier=GroupTier[tier.upper()],
                email="development@fluidattacks.com",
            )
            message = "Success"

    except ValueError as ex:
        message = "Invalid payload"
        status = "failed"
        LOGGER.exception(ex, extra=dict(extra=locals()))
    except SignatureVerificationError as ex:
        message = "Invalid signature"
        status = "failed"
        LOGGER.exception(ex, extra=dict(extra=locals()))

    return JSONResponse(
        {
            "status": status,
            "message": message,
        }
    )
