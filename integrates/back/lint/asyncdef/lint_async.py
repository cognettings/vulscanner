from api import (
    API_PATH,
)
import ast
import logging
import logging.config
from pathlib import (
    Path,
)
import sys
from typing import (
    Tuple,
)

LOGGER = logging.getLogger(__name__)


def format_async_output_log(filename: str, line: int):
    return (
        "An asynchronous function that doesn't make use "
        + f"of await has been found in \n {filename}:{line}."
    )


def find_async_without_await(filepath: str) -> Tuple[bool, str]:
    """
    This function takes a python file, and parses it for a function
    declaration that in its implementation does not use an await instance.

    Args:
        filepath (str): Path of the file to be examined.

    Returns:
        bool: Determine if there is a function in the file
        declared as async without using await.
    """
    has_await = None
    line = 0

    with open(filepath, "r") as file:
        tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                line = node.lineno
                has_await = False
                for subnode in ast.walk(node):
                    if isinstance(subnode, ast.Await):
                        has_await = True
                        break
                if not has_await:
                    break
        return (
            (not has_await, filepath, line)
            if (has_await != None)
            else (None, None, None)
        )


def get_python_files(folderpath: str) -> Tuple[bool, str]:
    """
    This function gets the python file from a project folder
    and sends them to the function.

    Args:
        folderpath (str): Path to a project folder.

    Returns:
        bool: The status of the find_async_without_await function.
    """
    for itempath in Path(folderpath).rglob("*.py"):
        found_match, filename, line = find_async_without_await(itempath)
        if found_match:
            return (True, filename, line)

    return (False, None, None)


def main() -> None:
    found_match, filename, line = get_python_files(API_PATH)
    if found_match:
        LOGGER.error(format_async_output_log(filename, line))
        sys.exit(1)
    LOGGER.info("No async functions without await instances found!")


if __name__ == "__main__":
    main()
