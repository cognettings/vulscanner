import ctx
from pathlib import (
    Path,
)


def infere_path(file_name: str) -> str | None:
    for config_path in ctx.SKIMS_CONFIG.sast.include:
        if config_path[0] == "/":
            file_path = config_path
        else:
            file_path = str(
                Path(ctx.SKIMS_CONFIG.working_dir, config_path).resolve()
            )

        if file_path.split("/")[-1] == file_name:
            return file_path
    return None


def get_file_paths(file_names: set[str]) -> set[str]:
    file_paths: set[str] = set()
    for file_name in file_names:
        if file_path := infere_path(file_name):
            file_paths.add(file_path)
    return file_paths


def parse_properties(file_names: set[str], load_key: str) -> str | None:
    for path in get_file_paths(file_names):
        with open(path, "r", encoding="utf-8") as prop_file:
            for line in prop_file:
                line_split = line.split("=")
                if (len(line_split) == 2) and (
                    line_split[0] == load_key[1:-1]
                ):
                    return line_split[1].lower().replace("\n", "")

    return None
