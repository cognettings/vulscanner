from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from aioextensions import (
    collect,
    schedule,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    IntegratesBatchQueue,
    Product,
)
from custom_utils import (
    datetime as datetime_utils,
)
from custom_utils.filter_vulnerabilities import (
    filter_non_deleted,
    filter_non_zero_risk,
    filter_released_vulns,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    GitCloningStatus,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    IPRoot,
    Root,
    URLRoot,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_black,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from mailer import (
    groups as groups_mail,
)
from roots import (
    domain as roots_domain,
    update as roots_update,
    utils as roots_utils,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def deactivate_root(  # pylint: disable=too-many-locals
    *,
    info: GraphQLResolveInfo,
    root: Root,
    email: str,
    **kwargs: Any,
) -> None:
    group_name: str = kwargs["group_name"]
    loaders: Dataloaders = info.context.loaders
    reason: str = kwargs["reason"]
    other: str | None = kwargs.get("other") if reason == "OTHER" else None
    last_status_update = await roots_update.get_last_status_update(
        loaders,
        root.id,
    )
    historic_state_date = last_status_update.modified_date
    last_clone_date_msg: str = "Never cloned"
    last_root_state: str = "Unknow"
    activated_by = last_status_update.modified_by

    if (
        isinstance(root, GitRoot)
        and root.cloning.status != GitCloningStatus.UNKNOWN
    ):
        last_clone_date_msg = str(root.cloning.modified_date.date())
        last_root_state = root.cloning.status.value

    root_vulnerabilities = filter_released_vulns(
        await loaders.root_vulnerabilities.load(root.id)
    )
    root_vulnerabilities_nzr = filter_non_zero_risk(
        filter_non_deleted(root_vulnerabilities)
    )
    sast_vulns = [
        vuln
        for vuln in root_vulnerabilities_nzr
        if vuln.type == VulnerabilityType.LINES
    ]
    dast_vulns = [
        vuln
        for vuln in root_vulnerabilities_nzr
        if vuln.type != VulnerabilityType.LINES
    ]

    await collect(
        tuple(
            vulns_domain.close_by_exclusion(
                vulnerability=vuln,
                modified_by=email,
                loaders=loaders,
            )
            for vuln in root_vulnerabilities
        ),
        workers=32,
    )
    await roots_domain.deactivate_root(
        email=email,
        group_name=group_name,
        other=other,
        reason=reason,
        root=root,
    )
    if root.state.status != RootStatus.INACTIVE:
        if isinstance(root, GitRoot):
            refresh_toe = await batch_dal.put_action(
                action=Action.REFRESH_TOE_LINES,
                attempt_duration_seconds=7200,
                entity=group_name,
                subject=email,
                additional_info=root.state.nickname,
                product_name=Product.INTEGRATES,
                queue=IntegratesBatchQueue.SMALL,
                dependsOn=[
                    {
                        "jobId": (
                            await batch_dal.put_action(
                                action=Action.REMOVE_ROOTS,
                                entity=group_name,
                                subject=email,
                                queue=IntegratesBatchQueue.SMALL,
                                additional_info=root.state.nickname,
                                product_name=Product.INTEGRATES,
                            )
                        ).batch_job_id,
                        "type": "SEQUENTIAL",
                    },
                ],
            )

            group = await groups_domain.get_group(loaders, group_name)
            key = batch_dal.generate_key_to_dynamod(
                action_name=Action.UPDATE_ORGANIZATION_OVERVIEW.value,
                additional_info="*",
                entity=group.organization_id,
                subject="integrates@fluidattacks.com",
            )
            overview_action = await batch_dal.get_action(action_dynamo_pk=key)
            if not overview_action:
                await batch_dal.put_action(
                    action=Action.UPDATE_ORGANIZATION_OVERVIEW,
                    vcpus=1,
                    product_name=Product.INTEGRATES,
                    queue=IntegratesBatchQueue.SMALL,
                    additional_info="*",
                    entity=group.organization_id.lower().lstrip("org#"),
                    attempt_duration_seconds=7200,
                    subject="integrates@fluidattacks.com",
                    dependsOn=[
                        {
                            "jobId": refresh_toe.batch_job_id,
                            "type": "SEQUENTIAL",
                        },
                    ],
                )

        if isinstance(root, (GitRoot, URLRoot)):
            await batch_dal.put_action(
                action=Action.REFRESH_TOE_INPUTS,
                entity=group_name,
                subject=email,
                additional_info=root.state.nickname,
                product_name=Product.INTEGRATES,
                queue=IntegratesBatchQueue.SMALL,
            )
        if isinstance(root, IPRoot):
            await batch_dal.put_action(
                action=Action.REFRESH_TOE_PORTS,
                entity=group_name,
                subject=email,
                additional_info=root.state.nickname,
                product_name=Product.INTEGRATES,
                queue=IntegratesBatchQueue.SMALL,
            )
    await update_unreliable_indicators_by_deps(
        EntityDependency.deactivate_root,
        finding_ids=list({vuln.finding_id for vuln in root_vulnerabilities}),
        root_ids=[(root.group_name, root.id)],
        vulnerability_ids=[vuln.id for vuln in root_vulnerabilities],
    )
    root_age = (datetime_utils.get_utc_now() - historic_state_date).days

    schedule(
        groups_mail.send_mail_deactivated_root(
            loaders=loaders,
            activated_by=activated_by,
            group_name=group_name,
            last_clone_date_msg=last_clone_date_msg,
            last_root_state=last_root_state,
            other=other,
            reason=reason,
            root_age=root_age,
            root_nickname=root.state.nickname,
            sast_vulns=len(sast_vulns),
            dast_vulns=len(dast_vulns),
            responsible=email,
        )
    )


@MUTATION.field("deactivateRoot")
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    email: str = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    root = await roots_utils.get_root(
        loaders, kwargs["id"], kwargs["group_name"]
    )

    if isinstance(root, GitRoot):
        await require_service_white(deactivate_root)(
            info=info, root=root, email=email, **kwargs
        )
    else:
        await require_service_black(deactivate_root)(
            info=info, root=root, email=email, **kwargs
        )

    return SimplePayload(success=True)
