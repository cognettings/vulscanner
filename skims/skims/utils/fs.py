import aiofiles
from collections.abc import (
    Awaitable,
    Callable,
    Iterator,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
from fnmatch import (
    fnmatch as matches_glob,
)
from glob import (
    iglob as glob,
)
from itertools import (
    chain,
)
from model.graph import (
    GraphShardMetadataLanguage,
)
from more_itertools import (
    collapse,
)
from operator import (
    attrgetter,
    methodcaller,
)
import os
from pyparsing import (
    Regex,
)
from utils.logs import (
    log_blocking,
)

MAX_FILE_SIZE: int = int(os.getenv('MAX_FILE_SIZE', 102400)) # default to 100 KiB


class FileTooLarge(Exception):
    pass


language_extensions_map: dict[GraphShardMetadataLanguage, list[str]] = {
    GraphShardMetadataLanguage.CSHARP: [".cs"],
    GraphShardMetadataLanguage.DART: [".dart"],
    GraphShardMetadataLanguage.GO: [".go"],
    GraphShardMetadataLanguage.HCL: [".hcl", ".tf"],
    GraphShardMetadataLanguage.JAVA: [".java"],
    GraphShardMetadataLanguage.JAVASCRIPT: [".js", ".jsx"],
    GraphShardMetadataLanguage.JSON: [".json"],
    GraphShardMetadataLanguage.KOTLIN: [".kt", ".ktm", ".kts"],
    GraphShardMetadataLanguage.PYTHON: [".py"],
    GraphShardMetadataLanguage.SWIFT: [".swift"],
    GraphShardMetadataLanguage.TYPESCRIPT: [".ts", ".tsx"],
    GraphShardMetadataLanguage.YAML: [".yaml", ".yml"],
}


def decide_language(path: str) -> GraphShardMetadataLanguage:
    for language, extensions in language_extensions_map.items():
        for extension in extensions:
            if path.endswith(extension):
                return language
    return GraphShardMetadataLanguage.NOT_SUPPORTED


def generate_file_content(
    path: str,
    encoding: str = "latin-1",
    size: int = -1,
) -> Callable[[], str]:
    data: dict[str, str] = {}

    def get_one() -> str:
        if not data:
            data["file_contents"] = get_file_content_block(
                path=path,
                encoding=encoding,
                size=size,
            )
        return data["file_contents"]

    return get_one


def generate_file_raw_content(
    path: str,
    size: int = -1,
) -> Callable[[], Awaitable[bytes]]:
    data: dict[str, bytes] = {}

    async def get_one() -> bytes:
        if not data:
            data["file_raw_content"] = await get_file_raw_content(path, size)
        return data["file_raw_content"]

    return get_one


def generate_file_raw_content_blocking(
    path: str,
    size: int = -1,
) -> Callable[[], bytes]:
    data: dict[str, bytes] = {}

    def get_one() -> bytes:
        if not data:
            data["file_raw_content"] = get_file_raw_content_blocking(
                path, size
            )
        return data["file_raw_content"]

    return get_one


async def get_file_content(
    path: str,
    encoding: str = "latin-1",
    size: int = -1,
) -> str:
    async with aiofiles.open(
        path,
        mode="r",
        encoding=encoding,
    ) as file_handle:
        file_contents: str = await file_handle.read(size)

        return file_contents


def get_file_content_block(
    path: str,
    encoding: str = "utf-8-sig",
    size: int = -1,
) -> str:
    with open(
        path,
        mode="r",
        encoding=encoding,
        errors="ignore",
    ) as file_handle:
        file_contents: str = file_handle.read(size)

        return file_contents


def sync_get_file_content(path: str, size: int = MAX_FILE_SIZE) -> str:
    if os.stat(path).st_size > MAX_FILE_SIZE:
        raise FileTooLarge(path)

    with open(path, mode="r", encoding="latin-1") as handle:
        content = handle.read(size)

    return content


async def get_file_raw_content(path: str, size: int = -1) -> bytes:
    async with aiofiles.open(path, mode="rb") as file_handle:
        file_contents: bytes = await file_handle.read(size)

        return file_contents


def get_file_raw_content_blocking(path: str, size: int = -1) -> bytes:
    with open(path, mode="rb") as file_handle:
        file_contents: bytes = file_handle.read(size)

        return file_contents


def sync_get_file_raw_content(path: str, size: int = MAX_FILE_SIZE) -> bytes:
    if os.stat(path).st_size > MAX_FILE_SIZE:
        raise FileTooLarge(path)

    with open(path, "rb") as handle:
        content = handle.read(size)

    return content


def safe_sync_get_file_raw_content(
    path: str, size: int = MAX_FILE_SIZE
) -> bytes | None:
    try:
        return sync_get_file_raw_content(path, size)
    except FileTooLarge:
        log_blocking("warning", "File too large: %s, ignoring", path)
        return None


def check_dependency_code(path: str) -> bool:
    language: GraphShardMetadataLanguage = decide_language(path)

    if language == GraphShardMetadataLanguage.JAVASCRIPT:
        regex_exp = [
            Regex(r"jQuery(.)*[Cc]opyright(.)*[Ll]icen"),
            Regex(r"[Cc]opyright(.)*[Ll]icen(.)*[Jj][Qq]uery"),
            Regex(r"[Aa]ngular[Jj][Ss](.)*[Gg]oogle(.)*[Ll]icen"),
        ]
    else:
        return False

    file_content = generate_file_content(path, size=200)
    raw_content = file_content()
    content = raw_content.replace("\n", " ")

    for regex in regex_exp:
        for _ in regex.scanString(content):
            return True
    return False


def get_non_upgradable_paths(paths: set[str]) -> set[str]:
    nu_paths: set[str] = set()

    intellisense_refs = {
        os.path.dirname(path)
        for path in paths
        if path.endswith("Scripts/_references.js")
    }

    for path in paths:
        if (
            any(
                path.startswith(intellisense_ref)
                for intellisense_ref in intellisense_refs
            )
            or any(
                matches_glob(f"/{path}", glob)
                for glob in (
                    "*/Assets*/vendor/*",
                    "*/Assets*/lib/*",
                    "*/Assets*/js/*",
                    "*/Content*/jquery*",
                    "*/GoogleMapping*.js",
                    "*/Scripts*/bootstrap*",
                    "*/Scripts*/modernizr*",
                    "*/Scripts*/jquery*",
                    "*/Scripts*/popper*",
                    "*/Scripts*/vue*",
                    "*/wwwroot/lib*",
                )
            )
            or check_dependency_code(path)
        ):
            nu_paths.add(path)

    return nu_paths


def get_non_verifiable_paths(paths: set[str]) -> set[str]:
    nv_paths: set[str] = set()

    for path in paths:
        _, file_info = os.path.split(path)
        file_name, file_extension = os.path.splitext(file_info)
        file_extension = file_extension[1:]

        if (
            file_extension
            in {
                "aar",
                "apk",
                "bin",
                "class",
                "dll",
                "DS_Store",
                "exec",
                "hprof",
                "jar",
                "jasper",
                "pdb",
                "pyc",
                "exe",
            }
            or (file_name, file_extension)
            in {
                ("debug", "log"),
                ("org.eclipse.buildship.core.prefs"),
                (".classpath", ""),
                (".project", ""),
                (".vscode", ""),
            }
            or any(
                path.endswith(end)
                for end in (
                    ".cs.bak",
                    ".csproj.bak",
                    ".min.js",
                )
            )
            or any(
                string in path
                for string in (
                    "/.serverless_plugins/",
                    "/.settings/",
                )
            )
        ):
            nv_paths.add(path)

    return nv_paths


def mkdir(name: str, mode: int = 0o777, exist_ok: bool = False) -> None:
    return os.makedirs(name, mode=mode, exist_ok=exist_ok)


def recurse_dir(path: str) -> tuple[str, ...]:
    try:
        scanner = tuple(os.scandir(path))
    except (FileNotFoundError, NotADirectoryError):
        scanner = tuple()

    dirs = tuple(
        map(attrgetter("path"), filter(methodcaller("is_dir"), scanner))
    )
    files = tuple(
        map(attrgetter("path"), filter(methodcaller("is_file"), scanner))
    )
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as _worker:
        tree = tuple(
            chain(
                files,
                _worker.map(recurse_dir, dirs),
            )
        )

    return tree


def recurse_path(path: str) -> tuple[str, ...]:
    return (path,) if os.path.isfile(path) else recurse_dir(path)


def iter_glob_path(path: str) -> Iterator[str]:
    if path.startswith("glob(") and path.endswith(")"):
        yield from glob(path[5:-1], recursive=True)
    else:
        yield path


def list_paths(include: tuple[str, ...], exclude: tuple[str, ...]) -> set[str]:
    def evaluate(wkr: ThreadPoolExecutor, paths: tuple[str, ...]) -> set[str]:
        return {
            os.path.normpath(path)
            for path in collapse(
                wkr.map(
                    recurse_path,
                    chain.from_iterable(map(iter_glob_path, paths)),
                ),
                base_type=str,
            )
        }

    try:
        with ThreadPoolExecutor(max_workers=os.cpu_count()) as worker:
            all_paths = evaluate(worker, include) - evaluate(worker, exclude)
        return all_paths

    except FileNotFoundError as exc:
        raise SystemExit(f"File does not exist: {exc.filename}") from exc


def split_by_upgradable(paths: set[str]) -> tuple[set[str], set[str]]:
    try:
        nu_paths = get_non_upgradable_paths(paths)
        return nu_paths, paths - nu_paths

    except FileNotFoundError as exc:
        raise SystemExit(f"File does not exist: {exc.filename}") from exc


def split_by_verifiable(paths: set[str]) -> tuple[set[str], set[str]]:
    try:
        nv_paths = get_non_verifiable_paths(paths)
        return nv_paths, paths - nv_paths

    except FileNotFoundError as exc:
        raise SystemExit(f"File does not exist: {exc.filename}") from exc


def split_by_upgradable_and_veriable(
    paths: set[str],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    nu_paths, up_paths = split_by_upgradable(paths)
    nv_paths, ok_paths = split_by_verifiable(up_paths)
    return tuple(ok_paths), tuple(nu_paths), tuple(nv_paths)


def resolve_paths(
    include: tuple[str, ...],
    exclude: tuple[str, ...],
) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    return split_by_upgradable_and_veriable(list_paths(include, exclude))
