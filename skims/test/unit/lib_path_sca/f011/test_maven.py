from ..utils import (
    get_file_info_from_path,
)
from lib.sca.f011.maven import (
    maven_gradle,
    maven_pom_xml,
    maven_sbt,
)
from operator import (
    itemgetter,
)
import pytest
import re


@pytest.mark.skims_test_group("unittesting")
def test_maven_pom_xml() -> None:
    path = "skims/test/data/lib/sca/f011/frst_child/scdn_child/pom.xml"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = maven_pom_xml.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_info = {
        "junit:junit": "4.12",
        "com.newrelic.agent.java:newrelic-agent": "6.3.0",
        "org.springframework:spring-web": "5.3.2",
        "org.springframework.security:spring-security-core": "4.2.2.RELEASE",
        "axis:axis": "1.4",
        "org.mockito:mockito-core": "2.0.31-beta",
        "org.apache.camel:camel-xstream": "2.6.0",
        "ballerina:ballerina-lang": "1.2.14",
    }
    for product, version in pkg_info.items():
        try:
            next_dep = next(generator_dep)
            item_name = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
            break
        equal_props: bool = version == item_ver and product == item_name
        if not equal_props:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_maven_pom_xml_deps_modules() -> None:
    path = "skims/test/data/lib/sca/f011/frst_child/pom.xml"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = maven_pom_xml.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    pkg_info = {
        "batik:batik-transcoder": "1.0.0",
        "be.cylab:snakeyaml": "2.0.0",
    }
    for product, version in pkg_info.items():
        try:
            next_dep = next(generator_dep)
            item_name = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
            break
        equal_props: bool = version == item_ver and product == item_name
        if not equal_props:
            assertion = not assertion
            break

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_maven_gradle() -> None:
    path: str = "skims/test/data/lib/sca/f011/build.gradle"
    file_contents: str = get_file_info_from_path(path)
    generator_dep = maven_gradle.__wrapped__(  # type: ignore
        file_contents, path
    )
    assertion: bool = True
    packages = (
        ("io.springfox:springfox-swagger-ui", "2.6.1"),
        ("org.apache.logging.log4j:log4j-core", "2.13.2"),
        ("org.json:json", "20160810"),
        ("javax.mail:mail", "1.4"),
    )
    for product, version in packages:
        try:
            next_dep = next(generator_dep)
            pkg_item = itemgetter("item")(next_dep[0])
            item_ver = itemgetter("item")(next_dep[1])
        except StopIteration:
            assertion = not assertion
        if not (pkg_item == product and version == item_ver):
            assertion = not assertion

    assert assertion


@pytest.mark.skims_test_group("unittesting")
def test_maven_sbt() -> None:
    sbt_dep: re.Pattern[str] = re.compile(
        r'"(?P<pkg>[\w\.\-]+)"\s+%\s+"(?P<module>[\w\.\-]+)"'
        r'\s+%\s+"(?P<version>[\d\.]+)"'
    )
    path: str = "skims/test/data/lib/sca/f011/build.sbt"
    file_contents: str = get_file_info_from_path(path)
    content: list[str] = file_contents.splitlines()
    generator_dep = maven_sbt.__wrapped__(file_contents, path)  # type: ignore
    assertion: bool = True
    for line_num in [*range(3, 8), 10, *range(14, 18), *range(20, 22), 23]:
        if pkg_info := sbt_dep.search(content[line_num]):
            pkg_name = f'{pkg_info.group("pkg")}:{pkg_info.group("module")}'
            version = pkg_info.group("version")

            try:
                next_dep = next(generator_dep)
                pkg_item = itemgetter("item")(next_dep[0])
                item = itemgetter("item")(next_dep[1])
            except StopIteration:
                assertion = not assertion
                break
            if not (pkg_item in pkg_name and version == item):
                assertion = not assertion
                break

    assert assertion
