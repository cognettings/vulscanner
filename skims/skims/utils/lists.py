def rm_duplicated(target: list) -> list:
    return list(dict.fromkeys(target))


def remove_last_slash(input_str: str) -> str:
    if input_str.endswith("/"):
        input_str = input_str[:-1]
    return input_str
