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
    Dataloaders,
    get_new_context,
)
from groups.domain import (
    get_closed_vulnerabilities,
    get_open_vulnerabilities,
)


@alru_cache(maxsize=None, typed=True)
async def generate_one(group: str) -> int:
    loaders: Dataloaders = get_new_context()
    open_vulnerabilities: int = await get_open_vulnerabilities(loaders, group)
    closed_vulnerabilities: int = await get_closed_vulnerabilities(
        loaders, group
    )

    return closed_vulnerabilities + open_vulnerabilities


if __name__ == "__main__":
    run(
        generate_all(
            get_data_one_group=generate_one,
            header="Total vulnerabilities",
        )
    )
