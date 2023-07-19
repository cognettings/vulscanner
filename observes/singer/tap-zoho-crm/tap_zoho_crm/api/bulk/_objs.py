from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from fa_purity import (
    Result,
    ResultE,
)
from typing import (
    IO,
    Optional,
)

JSONstr = str


class ModuleName(Enum):
    LEADS = "Leads"
    ACCOUNTS = "Accounts"
    CONTACTS = "Contacts"
    DEALS = "Deals"
    CAMPAIGNS = "Campaigns"
    TASKS = "Tasks"
    CASES = "Cases"
    CALLS = "Calls"
    SOLUTIONS = "Solutions"
    PRODUCTS = "Products"
    VENDORS = "Vendors"
    PRICE_BOOKS = "Price_Books"
    QUOTES = "Quotes"
    SALES_ORDERS = "Sales_Orders"
    PURCHASE_ORDERS = "Purchase_Orders"
    INVOICES = "Invoices"

    @staticmethod
    def from_raw(raw: str) -> ResultE[ModuleName]:
        try:
            return Result.success(ModuleName(raw))
        except ValueError as err:
            return Result.failure(Exception(err))


@dataclass(frozen=True)
class BulkJobResult:
    page: int
    count_items: int
    download_url: str
    more_records: bool


@dataclass(frozen=True)
class BulkJobId:
    job_id: str


@dataclass(frozen=True)
class BulkJob:
    operation: str
    created_by: JSONstr
    created_time: str
    state: str
    module: ModuleName
    page: int
    result: Optional[BulkJobResult] = None


@dataclass(frozen=True)
class BulkJobObj:
    job_id: BulkJobId
    job: BulkJob


@dataclass(frozen=True)
class BulkData:
    job_id: BulkJobId
    file: IO[str]
