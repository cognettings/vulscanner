import authz
from pandas import (
    DataFrame,
)


def create_dataframe(
    dataset: dict[str, list[str]],
    columns: list[str],
    rows: list[str],
    filename: str,
) -> None:
    dataframe = DataFrame(dataset, columns=columns, index=rows)
    html_matrix = dataframe.to_html()

    with open(
        "back/deploy/permissions_matrix/" + filename + ".html",
        "w",
        encoding="utf-8",
    ) as text_file:
        text_file.write(html_matrix)


def fill_matrix(
    roles_and_permissions: authz.model.types.RoleModel,
    columns: list[str],
    all_actions: list[str],
) -> dict[str, list[str]]:
    dataset = {}
    for role in columns:
        values = []
        for action in all_actions:
            is_action = (
                "X"
                if action in roles_and_permissions[role]["actions"]
                else " "
            )
            values.append(is_action)
        dataset[role] = values
    return dataset


def get_matrix_parameters(
    roles_and_permissions: authz.model.types.RoleModel, filename: str
) -> None:
    all_actions = []
    columns = list(roles_and_permissions.keys())
    roles_lenght = {}
    for role in columns:
        role_actions = roles_and_permissions[role]["actions"]
        roles_lenght[role] = len(role_actions)
        for action in role_actions:
            all_actions.append(action)
    all_actions = sorted(set(all_actions))
    sorted_columns = sorted(
        roles_lenght.keys(), key=lambda k: roles_lenght[k], reverse=True
    )
    dataset = fill_matrix(roles_and_permissions, sorted_columns, all_actions)

    create_dataframe(dataset, sorted_columns, all_actions, filename)


# Matrix for common permissions
get_matrix_parameters(authz.GROUP_LEVEL_ROLES, "group_level")
get_matrix_parameters(authz.ORGANIZATION_LEVEL_ROLES, "organization_level")
get_matrix_parameters(authz.USER_LEVEL_ROLES, "user_level")
