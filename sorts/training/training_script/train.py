#!/usr/bin/env python3

import argparse
from imblearn.over_sampling import (
    RandomOverSampler,
)
from itertools import (
    combinations,
)
import os
from pandas import (
    DataFrame,
)
from sklearn.utils import (
    shuffle,
)
from sorts.typings import (
    Model as ModelType,
)
from training.constants import (
    FEATURES_DICTS,
    MODELS,
    MODELS_DEFAULTS,
    RESULT_HEADERS,
)
from training.training_script.utils import (
    get_best_combination,
    load_training_data,
    save_model_to_s3,
    split_training_data,
    train_combination,
    update_results_csv,
)
from typing import (
    Generator,
    List,
    Tuple,
    Union,
)


def get_features_combinations(features: List[str]) -> List[Tuple[str, ...]]:
    feature_combinations: List[Tuple[str, ...]] = []
    # Use only 5 or more features in a combination as these have gotten
    # better results
    for idx in range(5, len(features) + 1):
        feature_combinations += list(combinations(features, idx))
    return list(filter(None, feature_combinations))


def get_model_instance(model_class: ModelType) -> ModelType:
    default_args: dict[str, Union[str, int, float]] = {"random_state": 42}
    model_defaults = MODELS_DEFAULTS.get(model_class, {})
    default_args.update(model_defaults)

    return model_class(**default_args)


def save_model(
    model_class: ModelType,
    training_dir: str,
    training_results: List[List[str]],
) -> None:
    best_features, best_f1 = get_best_combination(training_results)

    if best_features:
        shuffled_training_data = (
            load_training_data(training_dir)
            .sample(frac=1, random_state=42)
            .reset_index(drop=True)
        )
        train_x, train_y = split_training_data(
            shuffled_training_data, best_features
        )
        ros = RandomOverSampler(random_state=42)
        os_train_x, os_train_y = ros.fit_resample(train_x, train_y)
        shuffled_os_train_x, shuffled_os_train_y = shuffle(
            os_train_x, os_train_y, random_state=42
        )

        model = get_model_instance(model_class)
        model.fit(shuffled_os_train_x, shuffled_os_train_y)
        model_file_name: str = "-".join(
            [type(model).__name__.lower(), best_f1]
            + [FEATURES_DICTS[feature].lower() for feature in best_features]
        )
        model.feature_names = list(best_features)
        model.precision = training_results[-1][2]
        model.recall = training_results[-1][3]
        save_model_to_s3(model, model_file_name)


def split_list(
    list_to_split: List[Tuple[str, ...]], chunk_size: int
) -> Generator[List[Tuple[str, ...]], object, None]:
    for i in range(0, len(list_to_split), chunk_size):
        yield list_to_split[i : i + chunk_size]


def train_model(
    model_class: ModelType,
    training_dir: str,
    job_index: int,
) -> List[List[str]]:
    all_combinations = get_features_combinations(list(FEATURES_DICTS.keys()))
    split_combinations_list = list(split_list(all_combinations, 16))
    training_data: DataFrame = load_training_data(training_dir)
    shuffled_training_data = training_data.sample(
        frac=1, random_state=42
    ).reset_index(drop=True)
    training_output: list[list[str]] = [RESULT_HEADERS]

    # Train the model
    for combination in split_combinations_list[job_index]:
        model = get_model_instance(model_class)
        training_combination_output: list[str] = train_combination(
            model, shuffled_training_data, combination
        )
        training_output.append(training_combination_output)

    return training_output


def cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    # Sagemaker specific arguments. Defaults are set in environment variables.
    parser.add_argument(
        "--output-data-dir", type=str, default=os.environ["SM_OUTPUT_DATA_DIR"]
    )
    parser.add_argument(
        "--model-dir", type=str, default=os.environ["SM_MODEL_DIR"]
    )
    parser.add_argument(
        "--train", type=str, default=os.environ["SM_CHANNEL_TRAIN"]
    )

    # Model to train sent as a hyperparamenter
    parser.add_argument("--model", type=str, default="")
    parser.add_argument("--index", type=int, default=0)

    return parser.parse_args()


def main() -> None:
    args = cli()

    model_name: str = args.model
    model_class: ModelType = MODELS[model_name]

    # Start training process
    if model_class:
        results_filename: str = f"{model_name}_train_results_{args.index}.csv"
        training_output = train_model(model_class, args.train, args.index)
        update_results_csv(results_filename, training_output)
        save_model(model_class, args.train, training_output)


if __name__ == "__main__":
    main()
