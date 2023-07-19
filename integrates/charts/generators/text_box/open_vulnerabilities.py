from aioextensions import (
    run,
)
from async_lru import (
    alru_cache,
)
from charts.generators.text_box.utils import (
    generate_all,
)
from dataloaders import (
    get_new_context,
)
from groups.domain import (
    get_open_vulnerabilities,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    return await get_open_vulnerabilities(get_new_context(), group)


if __name__ == "__main__":
    run(
        generate_all(
            get_data_one_group=generate_one,
            header="Open Vulnerabilities",
        )
    )
