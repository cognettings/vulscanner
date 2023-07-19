from collections.abc import (
    Callable,
    Iterator,
)
import ctx
from model import (
    core,
)
from pyparsing import (
    col,
    makeHTMLTags,
    ParseException,
    ParserElement,
)
from serializers import (
    make_snippet,
    SnippetViewport,
)
from typing import (
    Any,
    NamedTuple,
    TypeVar,
)
from utils.function import (
    shield,
    shield_blocking,
)
from vulnerabilities import (
    build_lines_vuln,
    build_metadata,
)
from zone import (
    t,
)

# Constants
Tfun = TypeVar("Tfun", bound=Callable[..., Any])

NAMES_DOCKERFILE: set[str] = {"Dockerfile"}
EXTENSIONS_BASH: set[str] = {"sh"}
EXTENSIONS_CSHARP: set[str] = {"cs"}
EXTENSIONS_JAVA: set[str] = {"java"}
EXTENSIONS_JAVA_PROPERTIES: set[str] = {"properties"}
EXTENSIONS_JAVASCRIPT: set[str] = {"js", "jsx", "ts", "tsx"}
EXTENSIONS_JSON: set[str] = {"json"}
EXTENSIONS_PYTHON: set[str] = {"py", "pyw"}
EXTENSIONS_SWIFT: set[str] = {"swift"}
EXTENSIONS_YAML: set[str] = {"yml", "yaml"}
TRUE_OPTIONS: set[
    str | bool | int
] = {  # NOSONAR # pylint: disable=duplicate-value
    "true",
    "True",
    True,  # NOSONAR
    "1",
    1,
}
FALSE_OPTIONS: set[
    str | bool | int
] = {  # NOSONAR # pylint: disable=duplicate-value
    "false",
    "False",
    False,  # NOSONAR
    "0",
    0,
}

SHIELD: Callable[[Tfun], Tfun] = shield(on_error_return=())
SHIELD_BLOCKING: Callable[[Tfun], Tfun] = shield_blocking(on_error_return=())

# Lint config
# pylint: disable=too-many-arguments


class NpmDepInfo(NamedTuple):
    version: str
    product_line: int
    version_line: int


def has_attributes(content: str, tag: str, attrs: dict) -> bool:
    """
    Check ``HTML`` attributes` values.

    This method checks whether the tag (``tag``) inside the code file
    has attributes (``attr``) with the specific values.

    :param tag: ``HTML`` tag to search.
    :param attrs: Attributes with values to search.
    :returns: True if attribute set as specified, False otherwise.
    """

    tag_s, _ = makeHTMLTags(tag)
    tag_expr = tag_s

    result = False

    for expr in tag_expr.searchString(content):
        for attr, value in attrs.items():
            try:
                value.parseString(getattr(expr, attr))
                result = True
            except ParseException:
                result = False
                break
        if result:
            break

    return result


def get_matching_lines_blocking(
    content: str,
    grammar: ParserElement,
) -> list[core.GrammarMatch]:
    # Pyparsing's scanString expands tabs to 'n' number of spaces
    # But we count tabs as '1' char width
    # This forces the parser to not offset when a file contains tabs
    grammar.parseWithTabs()
    matches: list[core.GrammarMatch] = []
    for idx, line in enumerate(content.splitlines()):
        if len(line) < 1000:  # Avoid DoS for regex analyzing minified files
            matches += [
                core.GrammarMatch(
                    start_column=col(start_char, content) - 1,
                    start_line=idx + 1,
                )
                for _, start_char, _ in grammar.scanString(line)
            ]

    return matches


def get_vulnerabilities_blocking(
    content: str,
    description_key: str,
    grammar: ParserElement,
    path: str,
    method: core.MethodsEnum,
    wrap: bool = False,
) -> core.Vulnerabilities:
    results: core.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=path,
            where=str(match.start_line),
            metadata=build_metadata(
                method=method,
                description=f"{t(key=description_key)} {t(key='words.in')} "
                f"{ctx.SKIMS_CONFIG.namespace}/{path}",
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(
                        column=match.start_column,
                        line=match.start_line,
                        wrap=wrap,
                    ),
                ).content,
            ),
        )
        for match in get_matching_lines_blocking(content, grammar)
    )

    return results


def get_vulnerabilities_from_iterator_blocking(
    content: str,
    description_key: str,
    iterator: Iterator[tuple[int, int]],
    path: str,
    method: core.MethodsEnum,
) -> core.Vulnerabilities:
    results: core.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=path,
            where=str(line_no),
            metadata=build_metadata(
                method=method,
                description=f"{t(key=description_key)} {t(key='words.in')} "
                f"{ctx.SKIMS_CONFIG.namespace}/{path}",
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=column_no, line=line_no),
                ).content,
            ),
        )
        for line_no, column_no in iterator
    )

    return results


def get_vulnerabilities_include_parameter(
    content: str,
    description_key: str,
    iterator: Iterator[tuple[int, int, str]],
    path: str,
    method: core.MethodsEnum,
) -> core.Vulnerabilities:
    results: core.Vulnerabilities = tuple(
        build_lines_vuln(
            method=method,
            what=path,
            where=str(line_no),
            metadata=build_metadata(
                method=method,
                description=(
                    t(
                        key=(description_key),
                        port=param,
                    )
                    + f" {t(key='words.in')} "
                    f"{ctx.SKIMS_CONFIG.namespace}/{path}"
                ),
                snippet=make_snippet(
                    content=content,
                    viewport=SnippetViewport(column=column_no, line=line_no),
                ).content,
            ),
        )
        for line_no, column_no, param in iterator
    )

    return results


def filetypes_to_check_credentials(
    file_name: str, file_extension: str
) -> bool:
    files_types_to_check = {
        "env.dev",
        "env.development",
        "env.example",
        "env.local",
        "env.prod",
        "env.production",
    }
    complete_file_name = file_name + "." + file_extension
    quantity_of_periods = complete_file_name.count(".")
    if quantity_of_periods == 2:
        full_file_ext = complete_file_name[complete_file_name.find(".") + 1 :]
        if full_file_ext in files_types_to_check:
            return True
    return False
