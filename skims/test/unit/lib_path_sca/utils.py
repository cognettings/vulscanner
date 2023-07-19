def get_file_info_from_path(path: str) -> str:
    with open(
        path,
        mode="r",
        encoding="latin-1",
    ) as file_handle:
        file_contents: str = file_handle.read(-1)
    return file_contents
