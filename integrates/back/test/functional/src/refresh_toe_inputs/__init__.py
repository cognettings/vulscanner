# pylint: disable=import-error
from _pytest.monkeypatch import (
    MonkeyPatch,
)
from back.test.functional.src.utils import (
    get_batch_job,
    get_graphql_result,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    Product,
)
from batch_dispatch import (
    dispatch,
)
from dataloaders import (
    get_new_context,
)
import sys
from typing import (
    Any,
)


async def refresh_toe_inputs(
    *,
    user: str,
    group_name: str,
    monkeypatch: MonkeyPatch,
) -> None:
    await batch_dal.put_action(
        action=Action.REFRESH_TOE_INPUTS,
        entity=group_name,
        subject=user,
        additional_info="*",
        product_name=Product.INTEGRATES,
        queue=IntegratesBatchQueue.SMALL,
    )
    batch_action = await get_batch_job(
        action_name="refresh_toe_inputs", entity=group_name
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "test",
            batch_action.key,
        ],
    )
    await dispatch.dispatch()


async def query_get(
    *,
    user: str,
    group_name: str,
) -> dict[str, Any]:
    query: str = f"""{{
        group(groupName: "{group_name}"){{
            toeInputs {{
                edges {{
                    node {{
                       attackedAt
                        attackedBy
                        bePresent
                        bePresentUntil
                        component
                        entryPoint
                        firstAttackAt
                        seenAt
                        seenFirstTimeBy
                        root {{
                            ... on GitRoot {{
                            __typename
                            id
                            nickname
                            }}
                            ... on IPRoot {{
                            __typename
                            id
                            nickname
                            }}
                            ... on URLRoot {{
                            __typename
                            id
                            nickname
                            }}
                        }}
                    }}
                    cursor
                }}
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
            }}
        }}
      }}
    """
    data: dict[str, Any] = {"query": query}
    return await get_graphql_result(
        data,
        stakeholder=user,
        context=get_new_context(),
    )
