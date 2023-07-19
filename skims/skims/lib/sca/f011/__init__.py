from collections.abc import (
    Callable,
)
from lib.sca.common import (
    SHIELD_BLOCKING,
)
from lib.sca.f011.composer import (
    composer_json,
    composer_lock,
)
from lib.sca.f011.conan import (
    conan_conanfile_txt,
    conan_lock,
)
from lib.sca.f011.gem import (
    gem_gemfile,
    gem_gemfile_lock,
)
from lib.sca.f011.go import (
    go_mod,
)
from lib.sca.f011.maven import (
    get_pom_xml,
    maven_gradle,
    maven_pom_xml,
    maven_sbt,
)
from lib.sca.f011.npm import (
    npm_package_json,
    npm_package_lock_json,
    npm_yarn_lock,
)
from lib.sca.f011.nuget import (
    nuget_csproj,
    nuget_pkgs_config,
)
from lib.sca.f011.pip import (
    pip_requirements_txt,
)
from lib.sca.f011.pub import (
    pub_pubspec_yaml,
)
from model.core import (
    Vulnerabilities,
)


@SHIELD_BLOCKING
def run_composer_json(content: str, path: str) -> Vulnerabilities:
    return composer_json(content, path)


@SHIELD_BLOCKING
def run_composer_lock(content: str, path: str) -> Vulnerabilities:
    return composer_lock(content, path)


@SHIELD_BLOCKING
def run_conan_conanfile_txt(content: str, path: str) -> Vulnerabilities:
    return conan_conanfile_txt(content, path)


@SHIELD_BLOCKING
def run_conan_lock(content: str, path: str) -> Vulnerabilities:
    return conan_lock(content, path)


@SHIELD_BLOCKING
def run_gem_gemfile(content: str, path: str) -> Vulnerabilities:
    return gem_gemfile(content, path)


@SHIELD_BLOCKING
def run_gem_gemfile_lock(content: str, path: str) -> Vulnerabilities:
    return gem_gemfile_lock(content, path)


@SHIELD_BLOCKING
def run_go_mod(content: str, path: str) -> Vulnerabilities:
    return go_mod(content, path)


@SHIELD_BLOCKING
def run_maven_pom_xml(content: str, path: str) -> Vulnerabilities:
    return maven_pom_xml(content, path)


@SHIELD_BLOCKING
def run_maven_gradle(content: str, path: str) -> Vulnerabilities:
    return maven_gradle(content, path)


@SHIELD_BLOCKING
def run_maven_sbt(content: str, path: str) -> Vulnerabilities:
    return maven_sbt(content, path)


@SHIELD_BLOCKING
def run_npm_yarn_lock(content: str, path: str) -> Vulnerabilities:
    return npm_yarn_lock(content, path)


@SHIELD_BLOCKING
def run_nuget_csproj(content: str, path: str) -> Vulnerabilities:
    return nuget_csproj(content, path)


@SHIELD_BLOCKING
def run_nuget_pkgs_config(content: str, path: str) -> Vulnerabilities:
    return nuget_pkgs_config(content, path)


@SHIELD_BLOCKING
def run_npm_package_json(content: str, path: str) -> Vulnerabilities:
    return npm_package_json(content, path)


@SHIELD_BLOCKING
def run_npm_package_lock_json(content: str, path: str) -> Vulnerabilities:
    return npm_package_lock_json(content, path)


@SHIELD_BLOCKING
def run_pip_requirements_txt(content: str, path: str) -> Vulnerabilities:
    return pip_requirements_txt(content, path)


@SHIELD_BLOCKING
def run_pub_pubspec_yaml(content: str, path: str) -> Vulnerabilities:
    return pub_pubspec_yaml(content, path)


@SHIELD_BLOCKING
def analyze(  # noqa: MC0001
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    if file_extension == "xml" and get_pom_xml(content_generator()):
        return (run_maven_pom_xml(content_generator(), path),)

    if file_extension == "gradle":
        return (run_maven_gradle(content_generator(), path),)

    if (file_name, file_extension) == ("build", "sbt"):
        return (run_maven_sbt(content_generator(), path),)

    if (file_name, file_extension) == ("yarn", "lock"):
        return (run_npm_yarn_lock(content_generator(), path),)

    if file_extension == "csproj":
        return (run_nuget_csproj(content_generator(), path),)

    return analyze_2(content_generator, file_name, file_extension, path)


@SHIELD_BLOCKING
def analyze_2(  # noqa: MC0001
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    if (file_name, file_extension) == ("packages", "config"):
        return (run_nuget_pkgs_config(content_generator(), path),)

    if (file_name, file_extension) == ("package", "json"):
        return (run_npm_package_json(content_generator(), path),)

    if (file_name, file_extension) == ("package-lock", "json"):
        return (run_npm_package_lock_json(content_generator(), path),)

    if (file_name, file_extension) == ("requirements", "txt"):
        return (run_pip_requirements_txt(content_generator(), path),)

    if (file_name, file_extension) == ("Gemfile", "lock"):
        return (run_gem_gemfile_lock(content_generator(), path),)

    return analyze_3(content_generator, file_name, file_extension, path)


@SHIELD_BLOCKING
def analyze_3(  # noqa: MC0001
    content_generator: Callable[[], str],
    file_name: str,
    file_extension: str,
    path: str,
    **_: None,
) -> tuple[Vulnerabilities, ...]:
    # pylint: disable=too-many-return-statements
    if file_name == "Gemfile":
        return (run_gem_gemfile(content_generator(), path),)

    if (file_name, file_extension) == ("pubspec", "yaml"):
        return (run_pub_pubspec_yaml(content_generator(), path),)

    if (file_name, file_extension) == ("composer", "json"):
        return (run_composer_json(content_generator(), path),)

    if (file_name, file_extension) == ("composer", "lock"):
        return (run_composer_lock(content_generator(), path),)

    if (file_name, file_extension) == ("go", "mod"):
        return (run_go_mod(content_generator(), path),)

    if (file_name, file_extension) == ("conanfile", "txt"):
        return (run_conan_conanfile_txt(content_generator(), path),)

    if (file_name, file_extension) == ("conan", "lock"):
        return (run_conan_lock(content_generator(), path),)

    return ()
