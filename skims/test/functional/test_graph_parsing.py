from model.graph import (
    GraphDB,
)
import os
import pytest
from sast.parse import (
    _get_content,
    parse_one,
)
from utils.encodings import (
    json_dumps,
)
from utils.fs import (
    decide_language,
)


@pytest.mark.asyncio
@pytest.mark.skims_test_group("graph_generation")
@pytest.mark.parametrize(
    "files_to_test,suffix_out",
    [
        (
            (
                "skims/test/data/graphs/owasp/App.java",
                "skims/test/data/graphs/owasp/User.java",
                "skims/test/data/graphs/owasp/Test001.java",
                "skims/test/data/graphs/owasp/Test008.java",
                "skims/test/data/graphs/owasp/Test167.java",
            ),
            "benchmark",
        ),
        (
            (
                "skims/test/data/graphs/syntax/test_cfg.json",
                "skims/test/data/graphs/syntax/test_cfg.tf",
                "skims/test/data/graphs/syntax/test_cfg.yaml",
            ),
            "cfg_path",
        ),
        (
            (
                "skims/test/data/graphs/nist/CWE89_SQL_Injection.cs",
                "skims/test/data/graphs/nist/StudentController.cs",
                "skims/test/data/graphs/nist/HouseController.cs",
                "skims/test/data/graphs/nist/block_chaining_insecure.cs",
            ),
            "nist",
        ),
        (
            ("skims/test/data/graphs/syntax/syntax_cfg.cs",),
            "syntax_csharp",
        ),
        (
            ("skims/test/data/graphs/syntax/test_cfg.dart",),
            "syntax_dart",
        ),
        (
            ("skims/test/data/graphs/syntax/test_cfg.go",),
            "syntax_go",
        ),
        (
            ("skims/test/data/graphs/syntax/syntax_cfg.java",),
            "syntax_java",
        ),
        (
            ("skims/test/data/graphs/syntax/syntax_cfg.js",),
            "syntax_javascript",
        ),
        (
            ("skims/test/data/graphs/syntax/test_cfg.kt",),
            "syntax_kotlin",
        ),
        (
            ("skims/test/data/graphs/syntax/syntax_cfg.py",),
            "syntax_python",
        ),
        (
            ("skims/test/data/graphs/syntax/syntax_cfg.swift",),
            "syntax_swift",
        ),
        (
            ("skims/test/data/graphs/syntax/syntax_cfg.ts",),
            "syntax_typescript",
        ),
    ],
)
async def test_graph_generation(
    files_to_test: tuple[str, ...],
    suffix_out: str,
) -> None:
    working_dir = os.getcwd()
    # Test the GraphDB
    paths = tuple(sorted(files_to_test))

    graph_db = GraphDB(
        context={},
        shards={},
        shards_by_language_class={},
        shards_by_path={},
    )

    for path in paths:
        if (
            (language := decide_language(path))
            and (content := _get_content(path, working_dir))
            and (parsed := parse_one(path, language, content))
        ):
            graph_db.shards.update({parsed.path: parsed})

    graph_db_as_json_str = json_dumps(graph_db, indent=2, sort_keys=True)

    expected_path = os.path.join(
        os.environ["STATE"],
        f"skims/test/data/graphs/json_results/root-graph_{suffix_out}.json",
    )
    os.makedirs(os.path.dirname(expected_path), exist_ok=True)
    with open(expected_path, "w", encoding="utf-8") as handle:
        handle.write(graph_db_as_json_str)

    results_path = "skims/test/data/graphs/json_results/root-graph"
    with open(f"{results_path}_{suffix_out}.json", encoding="utf-8") as handle:
        assert graph_db_as_json_str == handle.read()
