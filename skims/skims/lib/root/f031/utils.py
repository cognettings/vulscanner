from utils.aws_iam import (
    match_pattern,
)


def match_iam_passrole(action: str) -> bool:
    return match_pattern(action, "iam:PassRole")


def action_has_full_access_to_ssm(actions: str | list) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    for action in actions_list:
        if action == "ssm:*":
            return True
    return False


def is_s3_action_writeable(actions: list | str) -> bool:
    actions_list = actions if isinstance(actions, list) else [actions]
    action_start_with = [
        "Copy",
        "Create",
        "Delete",
        "Put",
        "Restore",
        "Update",
        "Upload",
        "Write",
    ]
    for action in actions_list:
        if any(action.startswith(f"s3:{atw}") for atw in action_start_with):
            return True
    return False
