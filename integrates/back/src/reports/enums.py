from enum import (
    Enum,
)


class ReportType(str, Enum):
    CERT: str = "CERT"
    DATA: str = "DATA"
    PDF: str = "PDF"
    TOE_LINES: str = "TOE_LINES"
    XLS: str = "XLS"
