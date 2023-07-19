import click
import os
from sorts.association.file import (
    execute_association_rules,
)
from sorts.integrates.dal import (
    get_user_email,
)
from sorts.predict.file import (
    prioritize as prioritize_files,
)
from sorts.training.file import (
    get_subscription_file_metadata,
)
from sorts.utils.bugs import (
    configure_bugsnag,
)
from sorts.utils.decorators import (
    shield,
)
from sorts.utils.logs import (
    log,
    log_to_remote_info,
    mixpanel_track,
)
import sys
import time
from training.redshift import (
    db as redshift,
)


@click.command(
    help="File prioritizer according to the likelihood of finding "
    "a vulnerability"
)
@click.argument(
    "subscription",
    type=click.Path(
        allow_dash=False,
        dir_okay=True,
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
    ),
)
@click.option(
    "--association-rules",
    is_flag=True,
    help="Assign vulnerability suggestions to all the subscription files",
)
@click.option(
    "--get-file-data",
    is_flag=True,
    help="Extract file features from the subscription to train ML models",
)
@click.option(
    "--token-fluidattacks",
    envvar="SORTS_TOKEN_FLUIDATTACKS",
    help="Fluid Attacks API token.",
    show_envvar=True,
)
@click.option(
    "--token-ci",
    envvar="SORTS_TOKEN_CI",
    help="API token for CI mode.",
    show_envvar=True,
)
@shield(on_error_return=False)
def execute_sorts(
    subscription: str,
    association_rules: bool,
    get_file_data: bool,
    token_fluidattacks: str,
) -> None:
    configure_bugsnag()
    start_time: float = time.time()
    success: bool = False
    if token_fluidattacks:
        user_email: str = get_user_email(token_fluidattacks)
        group: str = os.path.basename(os.path.normpath(subscription))
        if get_file_data:
            success = get_subscription_file_metadata(
                token_fluidattacks, subscription
            )
        elif association_rules:
            execute_association_rules(token_fluidattacks, group)
            success = True
        else:
            success = prioritize_files(subscription)

        execution_time: float = time.time() - start_time
        log_to_remote_info(
            msg=f"Success: {success}",
            subscription=subscription,
            time=f"Finished after {execution_time:.2f} seconds",
            get_file_data=get_file_data,  # type: ignore
            association_rules=association_rules,  # type: ignore
            user=user_email,
        )
        redshift.insert(
            "executions",
            {
                "group_name": subscription.split("/")[-1],
                "execution_time": execution_time,
            },
        )
        mixpanel_track(
            user_email,
            "sorts_execution",
            subscription=subscription,
            get_file_data=get_file_data,  # type: ignore
            association_rules=association_rules,  # type: ignore
        )
    else:
        log(
            "error",
            "Set the Fluid Attacks API token either using the "
            "--token-fluidattacks flag or the "
            "SORTS_TOKEN_FLUIDATTACKS environmental variable.",
        )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
    execute_sorts(prog_name="sorts")
