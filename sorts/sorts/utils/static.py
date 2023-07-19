from fnmatch import (
    fnmatch,
)
from joblib import (
    load,
)
import json
import numpy as np
import os
from os import (
    environ,
)
from os.path import (
    abspath,
    exists,
    join,
)
from sklearn.neural_network import (
    MLPClassifier,
)
from sklearn.svm import (
    LinearSVC,
)
from sorts.constants import (
    STATIC_DIR,
)


def filter_third_party_files(repo_paths: list[str]) -> list[str]:
    """Filter out all third party files"""
    filtered_paths: list[str] = []
    intellisense_refs = {
        os.path.dirname(path)
        for path in repo_paths
        if path.endswith("Scripts/_references.js")
    }
    for path in repo_paths:
        _, file_info = os.path.split(path)
        file_name, file_extension = os.path.splitext(file_info)
        file_extension = file_extension[1:]

        if (
            (file_name, file_extension)
            not in {
                ("debug", "log"),
                (".classpath", ""),
                (".project", ""),
            }
            and not any(
                path.endswith(end)
                for end in (
                    ".cs.bak",
                    ".csproj.bak",
                    ".min.js",
                )
            )
            and not any(
                string in path
                for string in (
                    "/.serverless_plugins/",
                    "/.settings/",
                )
            )
            and not any(
                path.startswith(intellisense_ref)
                for intellisense_ref in intellisense_refs
            )
            and not any(
                fnmatch(f"/{path}", glob)
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
        ):
            filtered_paths.append(path)

    return filtered_paths


def get_extensions_list() -> list[str]:
    """Returns a list with all the extensions allowed"""
    extensions: list[str] = []
    with open(get_static_path("extensions.lst"), "r", encoding="utf8") as file:
        extensions = [line.rstrip() for line in file]

    return extensions


def get_static_path(file: str) -> str:
    """Gets the absolute path in both local repository and installed package"""
    static_path: str = abspath(join(STATIC_DIR, file))
    if exists(static_path):
        return static_path

    raise FileNotFoundError(static_path)


def read_allowed_names() -> tuple[list[str], ...]:
    """Reads static lists containing allowed names and extensions"""
    allowed_names: list[list[str]] = []
    for name in ["extensions.lst", "composites.lst"]:
        with open(get_static_path(name), encoding="utf8") as file:
            content_as_list = file.read().split("\n")
            allowed_names.append(list(filter(None, content_as_list)))

    return (allowed_names[0], allowed_names[1])


def load_model() -> MLPClassifier:
    model_path: str = environ["SORTS_MODEL_PATH"]

    return load(model_path)


def load_support_vector_machine() -> LinearSVC:
    model = LinearSVC()
    with open(
        get_static_path("model_parameters.json"), "r", encoding="utf8"
    ) as mod:
        params = json.load(mod)
    model.coef_ = np.array(params["coef"])
    model.intercept_ = np.array(params["intercept"])
    model.classes_ = np.array(params["classes"])

    return model
