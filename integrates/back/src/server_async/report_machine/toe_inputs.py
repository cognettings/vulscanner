from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidRootComponent,
    RepeatedToeInput,
)
from dataloaders import (
    Dataloaders,
)
from dynamodb.types import (
    Item,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToAdd,
)
from urllib.parse import (
    urlparse,
)


async def ensure_toe_inputs(
    loaders: Dataloaders, group_name: str, root_id: str, stream: Item
) -> None:
    vulns_for_toe: list[Item] = [
        vuln
        for vuln in stream["inputs"]
        if vuln["state"] == "open" and vuln["skims_technique"] != "APK"
    ]
    if vulns_for_toe:
        for vuln in vulns_for_toe:
            url: str = vuln["url"].split(" ")[0]
            parsed_url = urlparse(url)
            with suppress(RepeatedToeInput):
                try:
                    await toe_inputs_domain.add(
                        loaders=loaders,
                        group_name=group_name,
                        component=url,
                        entry_point="",
                        attributes=ToeInputAttributesToAdd(
                            be_present=True,
                            unreliable_root_id=root_id,
                            has_vulnerabilities=False,
                            seen_first_time_by="machine@fluidattacks.com",
                        ),
                    )
                except InvalidRootComponent as exc:
                    env_urls = await loaders.root_environment_urls.load(
                        root_id
                    )
                    parsed_env_toes = [
                        urlparse(env_url.url) for env_url in env_urls
                    ]
                    # Some invalid component may be the same domain
                    # as a valid env_url but with different scheme,
                    # since Machine analyzes both the HTTP and HTTPS urls.
                    # Only break execution when this is not the case.
                    if (
                        len(
                            [
                                toe
                                for toe in parsed_env_toes
                                if (
                                    toe.scheme != parsed_url.scheme
                                    and toe.netloc == parsed_url.netloc
                                )
                            ]
                        )
                        == 0
                    ):
                        raise exc
