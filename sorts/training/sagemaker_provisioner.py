#!/usr/bin/env python3

from botocore.exceptions import (
    ClientError,
)
from concurrent.futures import (
    ThreadPoolExecutor,
)
import random
from sagemaker.sklearn import (
    SKLearn,
)
from sagemaker.sklearn.estimator import (
    SKLearn as SKLearnEstimator,
)
from training.constants import (
    DATASET_PATH,
    MODELS,
    PARALLEL_JOBS,
    RESULT_HEADERS,
    S3_BUCKET_NAME,
    S3_RESOURCE,
    SAGEMAKER_METRIC_DEFINITIONS,
)
from training.redshift import (
    db as redshift,
)
from training.training_script.utils import (
    get_previous_training_results,
    update_results_csv,
)


def get_estimator(
    model: str,
    job_type: str,
    job_index: int = 0,
    training_script: str = "training/training_script/train.py",
) -> SKLearnEstimator:
    hyperparameters = (
        {"model": model.split(":")[0], "index": job_index}
        if job_type == "training"
        else {"model": model.split(":")[0]}
    )
    sklearn_estimator: SKLearnEstimator = SKLearn(
        entry_point=training_script,
        dependencies=["sorts", "training", "training/requirements.txt"],
        framework_version="1.2-1",
        instance_count=1,
        role="arn:aws:iam::205810638802:role/prod_sorts",
        output_path="s3://sorts/training-output",
        base_job_name=f"sorts-training-test-{model.split(':')[0].lower()}",
        hyperparameters=hyperparameters,
        metric_definitions=SAGEMAKER_METRIC_DEFINITIONS,
        debugger_hook_config=False,
        instance_type="ml.m5.2xlarge",
        tags=[
            {"Key": "management:area", "Value": "cost"},
            {"Key": "management:product", "Value": "sorts"},
            {"Key": "management:type", "Value": "product"},
        ],
    )

    return sklearn_estimator


def deploy_training_job(model: str, job_index: int) -> None:
    print(f"Deploying training job for {model}...")
    sklearn_estimator: SKLearnEstimator = get_estimator(
        model, "training", job_index
    )
    sklearn_estimator.fit({"train": DATASET_PATH})


def process_training_results(model: str) -> None:
    model_results = [RESULT_HEADERS]

    for job_number in range(PARALLEL_JOBS):
        previous_results = get_previous_training_results(
            f"{model}_train_results_{job_number}.csv"
        )
        model_results = model_results + previous_results[1:]
        try:
            S3_RESOURCE.Object(
                S3_BUCKET_NAME,
                f"training-output/results/{model}"
                f"_train_results_{job_number}.csv",
            ).delete()
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                print(f"[INFO] Job number {job_number} could not finish")

    results_filename: str = f"{model}_train_results.csv"
    update_results_csv(results_filename, model_results)

    for result in model_results[1:]:
        combination_train_results = dict(
            model=result[0],
            features=result[1],
            precision=result[2],
            recall=result[3],
            f_score=result[4],
            overfit=result[6],
            tuned_parameters=result[7],
            training_time=result[8],
        )
        redshift.insert("training", combination_train_results)


if __name__ == "__main__":
    all_models: list[str] = list(MODELS.keys())
    models_to_train = random.choices(all_models, k=round(len(all_models) / 2))
    for model_name in models_to_train:
        with ThreadPoolExecutor(max_workers=PARALLEL_JOBS) as executor:
            executor.map(
                lambda x: deploy_training_job(*x),
                zip([model_name] * PARALLEL_JOBS, range(PARALLEL_JOBS)),
            )
        process_training_results(model_name)
