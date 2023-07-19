from collections.abc import (
    Callable,
)
from lib.sca.common import (
    SHIELD_BLOCKING,
)
from lib.sca.f393.composer import (
    composer_json_dev,
    composer_lock_dev,
)
from lib.sca.f393.conan import (
    conan_conanfile_txt_dev,
    conan_lock_dev,
)
from lib.sca.f393.gem import (
    gem_gemfile_dev,
)
from lib.sca.f393.npm import (
    npm_package_json,
    npm_pkg_lock_json,
    npm_yarn_lock_dev,
)
from lib.sca.f393.pub import (
    pub_pubspec_yaml_dev,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_composer_json_dev(content: str, path: str) -> Vulnerabilities:
    return composer_json_dev(content, path)


@SHIELD_BLOCKING
def run_composer_lock_dev(content: str, path: str) -> Vulnerabilities:
    return composer_lock_dev(content, path)


@SHIELD_BLOCKING
def run_conan_conanfile_txt_dev(content: str, path: str) -> Vulnerabilities:
    return conan_conanfile_txt_dev(content, path)


@SHIELD_BLOCKING
def run_conan_lock_dev(content: str, path: str) -> Vulnerabilities:
    return conan_lock_dev(content, path)


@SHIELD_BLOCKING
def run_gem_gemfile_dev(content: str, path: str) -> Vulnerabilities:
    return gem_gemfile_dev(content, path)


@SHIELD_BLOCKING
def run_npm_package_json(content: str, path: str) -> Vulnerabilities:
    return npm_package_json(content, path)


@SHIELD_BLOCKING
def run_npm_pkg_lock_json(content: str, path: str) -> Vulnerabilities:
    return npm_pkg_lock_json(content, path)


@SHIELD_BLOCKING
def run_npm_yarn_lock_dev(content: str, path: str) -> Vulnerabilities:
    return npm_yarn_lock_dev(content, path)


@SHIELD_BLOCKING
def run_pub_pubspec_yaml_dev(content: str, path: str) -> Vulnerabilities:
    return pub_pubspec_yaml_dev(content, path)


@SHIELD_BLOCKING
def analyze(
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    # pylint: disable=too-many-return-statements
    if (file_name, file_extension) == ("package", "json"):
        return (run_npm_package_json(content_generator(), path),)

    if (file_name, file_extension) == ("yarn", "lock"):
        return (run_npm_yarn_lock_dev(content_generator(), path),)

    if (file_name, file_extension) == ("package-lock", "json"):
        return (run_npm_pkg_lock_json(content_generator(), path),)

    if file_name == "Gemfile":
        return (run_gem_gemfile_dev(content_generator(), path),)

    if (file_name, file_extension) == ("pubspec", "yaml"):
        return (run_pub_pubspec_yaml_dev(content_generator(), path),)

    if (file_name, file_extension) == ("composer", "json"):
        return (run_composer_json_dev(content_generator(), path),)

    if (file_name, file_extension) == ("composer", "lock"):
        return (run_composer_lock_dev(content_generator(), path),)

    if (file_name, file_extension) == ("conanfile", "txt"):
        return (run_conan_conanfile_txt_dev(content_generator(), path),)

    if (file_name, file_extension) == ("conan", "lock"):
        return (run_conan_lock_dev(content_generator(), path),)
    return ()
