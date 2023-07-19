# type: ignore
import datetime
import glob
import json
from model import (
    core,
)
import os
import re
from utils.encodings import (
    yaml_dumps_blocking,
)

# Constants
FOLDER = "../owasp_benchmark"


def get_tests_cases() -> dict[str, list[str]]:
    tests = {}
    pattern = re.compile(
        r'@WebServlet\(value\s*=\s*"/(\w+)-',
        flags=re.MULTILINE,
    )
    test_files = sorted(
        glob.glob(
            f"{FOLDER}/src/main/java/org/owasp/benchmark/testcode/*.java",
        )
    )

    for test_file in test_files:
        with open(test_file, encoding="utf-8") as handle:
            content = handle.read()

        if match := pattern.search(content):
            category = match.group(1)
            tests.setdefault(category, [])
            tests[category].append(os.path.relpath(test_file, FOLDER))
        else:
            raise Exception(content)

    return tests


def main() -> None:
    year: str = datetime.datetime.now().strftime("%Y")
    suites: list[str] = []
    categories = {
        "cmdi": [core.FindingEnum.F004.name],
        "crypto": [core.FindingEnum.F052.name],
        "hash": [core.FindingEnum.F052.name],
        "ldapi": [core.FindingEnum.F107.name],
        "pathtraver": [core.FindingEnum.F063.name],
        "sqli": [core.FindingEnum.F112.name],
        "securecookie": [core.FindingEnum.F042.name],
        "trustbound": [core.FindingEnum.F089.name],
        "weakrand": [core.FindingEnum.F034.name],
        "xpathi": [core.FindingEnum.F021.name],
        "xss": [core.FindingEnum.F008.name],
    }
    extra_files: list[str] = [
        "src/main/java/org/owasp/benchmark/helpers/DatabaseHelper.java",
        "src/main/java/org/owasp/benchmark/helpers/SeparateClassRequest.java",
        "src/main/java/org/owasp/benchmark/helpers/Thing1.java",
        "src/main/java/org/owasp/benchmark/helpers/Thing2.java",
        "src/main/java/org/owasp/benchmark/helpers/ThingFactory.java",
        "src/main/resources/benchmark.properties",
    ]

    for category, tests_cases in get_tests_cases().items():
        tests_cases.sort()

        suite = f"benchmark_owasp_{category}"
        suites.append(suite)

        with open(
            f"skims/test/data/config/{suite}.yaml", "w", encoding="utf-8"
        ) as handle:
            handle.write(
                yaml_dumps_blocking(
                    dict(
                        checks=categories.get(category, []),
                        namespace="OWASP",
                        output=f"skims/test/outputs/{suite}.csv",
                        path=dict(
                            include=extra_files + tests_cases,
                            lib_path=category == "crypto",
                            lib_root=category != "crypto",
                        ),
                        working_dir=FOLDER,
                    )
                )
            )

    suite = "benchmark_owasp"
    with open(
        f"skims/test/data/config/{suite}.yaml", "w", encoding="utf-8"
    ) as handle:
        handle.write(
            yaml_dumps_blocking(
                dict(
                    checks=sorted(
                        set(
                            finding
                            for findings in categories.values()
                            for finding in findings
                        )
                    ),
                    namespace="OWASP",
                    output=f"Benchmark_1.2-Fluid-Attacks-v{year}.csv",
                    path=dict(
                        include=["."],
                    ),
                    working_dir=FOLDER,
                )
            )
        )

    print(json.dumps(suites, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
