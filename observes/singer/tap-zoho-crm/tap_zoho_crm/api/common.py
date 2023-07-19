from dataclasses import (
    dataclass,
)
from tap_zoho_crm.api.auth import (
    Token,
)

API_URL = "https://www.zohoapis.com"


class UnexpectedResponse(Exception):
    pass


@dataclass(frozen=True)
class PageIndex:
    page: int
    per_page: int


@dataclass(frozen=True)
class DataPageInfo:
    page: PageIndex
    n_items: int
    more_records: bool


__all__ = ["Token"]
