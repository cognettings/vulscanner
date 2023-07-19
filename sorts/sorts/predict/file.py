import os
import pandas as pd
from pandas import (
    DataFrame,
)
from sorts.constants import (
    S3_BUCKET,
)
from sorts.features.file import (
    extract_features,
)
from sorts.utils.logs import (
    log,
)
from sorts.utils.predict import (
    display_results,
    predict_vuln_prob,
)
from sorts.utils.repositories import (
    get_repository_files,
)
from sorts.utils.static import (
    filter_third_party_files,
    get_extensions_list,
    read_allowed_names,
)


def get_subscription_files_df(subscription_path: str) -> DataFrame:
    """Builds the basic DF with all the files from every repository"""
    files: list[str] = []
    extensions, composites = read_allowed_names()
    for repo in os.listdir(subscription_path):
        repo_files = get_repository_files(
            os.path.join(subscription_path, repo)
        )
        filtered_repo_files = filter_third_party_files(repo_files)
        allowed_files = list(
            filter(
                lambda x: (
                    x in composites or x.split(".")[-1].lower() in extensions
                ),
                filtered_repo_files,
            )
        )
        if allowed_files:
            files.extend(allowed_files)
    files_df: DataFrame = pd.DataFrame(files, columns=["file"])
    files_df["repo"] = files_df["file"].apply(
        lambda x: os.path.join(subscription_path, x.split("/")[0])
    )
    return files_df


def prioritize(subscription_path: str) -> bool:
    """Prioritizes files according to the chance of finding a vulnerability"""
    success: bool = False
    group_name: str = os.path.basename(os.path.normpath(subscription_path))
    if os.path.exists(subscription_path):
        predict_df: DataFrame = get_subscription_files_df(subscription_path)
        success = extract_features(predict_df)
        if success:
            extensions: list[str] = get_extensions_list()
            num_bits: int = len(extensions).bit_length()
            csv_name: str = f"{group_name}_sorts_results_file.csv"
            predict_vuln_prob(
                predict_df,
                [f"extension_{num}" for num in range(num_bits + 1)],
                csv_name,
            )
            S3_BUCKET.Object(
                f"sorts-execution-results/{csv_name}"
            ).upload_file(csv_name)
            display_results(csv_name)
    else:
        log(
            "error",
            "There is no repository folder",
        )

    return success
