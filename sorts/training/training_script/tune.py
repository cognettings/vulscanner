import argparse
import os
from pandas import (
    DataFrame,
)
from sorts.typings import (
    Model as ModelType,
)
from training.constants import (
    FEATURES_DICTS,
    MODEL_HYPERPARAMETERS,
    MODELS,
    MODELS_DEFAULTS,
    RESULT_HEADERS,
)
from training.training_script.utils import (
    get_current_model_features,
    get_previous_training_results,
    load_training_data,
    save_model_to_s3,
    split_training_data,
    train_combination,
    update_results_csv,
)
from typing import (
    Dict,
    List,
    Tuple,
    Union,
)


def train_model(
    model: ModelType,
    model_features: Tuple[str, ...],
    training_dir: str,
    results_filename: str,
    tuned_hyperparameters: str,
) -> List[List[str]]:
    training_data: DataFrame = load_training_data(training_dir)
    shuffled_training_data = training_data.sample(
        frac=1, random_state=42
    ).reset_index(drop=True)
    training_combination_output: list[str] = train_combination(
        model, shuffled_training_data, model_features, tuned_hyperparameters
    )
    previous_results = get_previous_training_results(results_filename)
    training_output: list[list[str]] = (
        previous_results if previous_results else [RESULT_HEADERS]
    )
    training_output.append(training_combination_output)

    return training_output


def save_model(
    model: ModelType,
    f1_score: float,
    model_features: Tuple[str, ...],
    tuned_hyperparameters: List[str],
) -> None:
    model_file_name: str = "-".join(
        [
            type(model).__name__.lower(),
            str(f1_score),
            "-".join(
                [FEATURES_DICTS[feature].lower() for feature in model_features]
            ),
            "tune",
            "-".join(
                list(str(parameter) for parameter in tuned_hyperparameters)
            ),
        ]
    )
    save_model_to_s3(model, model_file_name)


def get_model_hyperparameters(
    model_name: str, args: Dict[str, str]
) -> Dict[str, str]:
    model_hyperparameters = list(MODEL_HYPERPARAMETERS[model_name].keys())

    return {parameter: args[parameter] for parameter in model_hyperparameters}


def display_model_hyperparameters(
    model_name: str, hyperaparameters_list: Dict[str, str]
) -> None:
    print(
        f"We have the following hyperparameters "
        f"for our {model_name.upper()} model tuning:"
    )
    for parameter, value in hyperaparameters_list.items():
        print(f"{parameter}: {value}")


def check_max_leaf_nodes(value: str) -> Union[int, None]:
    if value != "0":
        return int(value)

    return None


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
    parser.add_argument("--model", type=str, default="")

    # MLPCLassifier parameters to tune
    parser.add_argument("--activation", type=str, default="")
    parser.add_argument("--solver", type=str, default="")

    # XGBoost parameters to tune
    parser.add_argument("--criterion", type=str, default="friedman_mse")
    parser.add_argument("--loss", type=str, default="deviance")
    parser.add_argument("--max_depth", type=int, default=3)
    parser.add_argument("--n_estimators", type=int, default=100)
    parser.add_argument("--learning_rate", type=float, default=0.1)

    # HistGradientBoostingClassifier parameters to tune
    parser.add_argument(
        "--max_leaf_nodes", type=check_max_leaf_nodes, default=31
    )

    return parser.parse_args()


def main() -> None:
    args = cli()

    model_name: str = args.model.split("-")[0]
    model_features: Tuple[str, ...] = get_current_model_features()

    hyperparameters_to_tune: dict[str, str] = get_model_hyperparameters(
        model_name,
        vars(args),
    )
    display_model_hyperparameters(model_name, hyperparameters_to_tune)
    model_class: ModelType = MODELS[model_name]
    model_parameters: dict[str, object] = {"random_state": 42}
    model_defaults = {
        **MODELS_DEFAULTS.get(model_class, {}),
        **hyperparameters_to_tune,
    }
    model_parameters.update(model_defaults)
    model: ModelType = model_class(**model_parameters)

    results_filename: str = f"{model_name}_tune_results.csv"

    # Start training process
    hyperparameters_to_tune_list = ", ".join(
        list(str(parameter) for parameter in hyperparameters_to_tune.values())
    )
    training_output = train_model(
        model,
        model_features,
        args.train,
        results_filename,
        hyperparameters_to_tune_list,
    )

    update_results_csv(results_filename, training_output)

    training_data: DataFrame = load_training_data(args.train)
    shuffled_training_data = training_data.sample(
        frac=1, random_state=42
    ).reset_index(drop=True)
    train_x, train_y = split_training_data(
        shuffled_training_data, model_features
    )
    model.fit(train_x, train_y)
    model.feature_names = list(model_features)
    model.precision = training_output[-1][2]
    model.recall = training_output[-1][3]

    save_model(
        model,
        float(training_output[-1][4]),
        model_features,
        list(hyperparameters_to_tune.values()),
    )


if __name__ == "__main__":
    main()
