from opentelemetry.trace import (
    get_current_span,
    INVALID_SPAN,
)


def is_root_span() -> bool:
    parent_span = get_current_span()
    return parent_span is INVALID_SPAN
