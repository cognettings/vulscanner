import contextlib


def load_java_properties(
    content: str,
    include_comments: bool = False,
    exclude_protected_values: bool = False,
) -> dict[int, tuple[str, str]]:
    mapping: dict[int, tuple[str, str]] = {}

    for line_no, line in enumerate(content.splitlines(), start=1):
        # Strip comments
        if not include_comments and "#" in line:
            line = line.split("#", maxsplit=1)[0]

        # Split in key and value
        with contextlib.suppress(ValueError):
            key, val = line.strip().split("=", maxsplit=1)
            key, val = key.strip(), val.strip()

            if (
                exclude_protected_values
                and val
                and any(
                    val.startswith(pattern)
                    for pattern in [
                        "${",  # env var
                        "ENC(",  # encrypted with Jasypt
                        "#{",  # encrypted with unknown tool
                        "(",  # functional comments in the code
                    ]
                )
            ):
                # We should not include this line because it's protected
                pass
            else:
                mapping[line_no] = (key, val)

    return mapping


def load_as_dict(
    content: str,
    include_comments: bool = False,
    exclude_protected_values: bool = False,
) -> dict[str, str]:
    data: dict[str, str] = dict(
        load_java_properties(
            content,
            include_comments,
            exclude_protected_values,
        ).values()
    )

    return data
