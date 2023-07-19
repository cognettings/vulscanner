from more_itertools import (
    chunked,
)
from serializers import (
    make_snippet,
    SNIPPETS_COLUMNS,
    SnippetViewport,
)


def _set_line(found: bool) -> int:
    return 0 if found else 1


def snippet(
    url: str,
    header: str | None,
    headers: dict[str, str],
    columns_per_line: int = SNIPPETS_COLUMNS,
    value: str = "",
) -> str:
    line: int = 3
    found: bool = False
    content: str = f"> GET {url}\n> ...\n\n"

    for key, val in headers.items():
        line += _set_line(found)
        if key == header and value in val:
            found = True

        if len(val) + len(key) + 6 > columns_per_line:
            content += f"< {key}:\n"
            for val_chunk in chunked(val, columns_per_line - 4):
                line += _set_line(found)
                content += "    " + "".join(val_chunk) + "\n"
        else:
            content += f"< {key}: {val}\n"

    content += "\n* EOF"

    if not found:
        line += 2

    return make_snippet(
        content=content,
        viewport=SnippetViewport(
            columns_per_line=columns_per_line,
            column=0,
            line=line,
            wrap=True,
        ),
    ).content
