import csv
import os
from training.evaluate_results import (
    get_model_item,
)
from training.training_script.train import (
    get_features_combinations,
)
from training.training_script.utils import (
    get_best_combination,
)

DATA_PATH: str = f"{os.path.dirname(__file__)}/data"


def test_get_best_combination() -> None:
    expected_results = {
        "best_features": (
            "seldom_contributors",
            "num_lines",
            "commit_frequency",
        ),
        "best_f1": "77.4",
    }
    with open(
        os.path.join(DATA_PATH, "test_model_train_results.csv"),
        "r",
        encoding="utf8",
    ) as csv_file:
        csv_reader = csv.reader(csv_file)
        best_features, best_f1 = get_best_combination(list(csv_reader))
        assert best_features == expected_results["best_features"]
        assert best_f1 == expected_results["best_f1"]


def test_get_features_combinations() -> None:
    expected_result = [
        (
            "num_commits",
            "file_age",
            "seldom_contributors",
            "num_lines",
            "commit_frequency",
        ),
    ]
    combinations = get_features_combinations(
        [
            "num_commits",
            "file_age",
            "seldom_contributors",
            "num_lines",
            "commit_frequency",
        ]
    )
    assert combinations == expected_result


def test_get_model_item() -> None:
    expected_item = {
        "model": "histgradientboostingclassifier",
        "f_score": 74,
        "features": "AU, LC",
        "tuned_parameters": "max_leaf_nodes:0, learning_rate:1",
    }
    item = get_model_item("histgradientboostingclassifier-74-au-lc-tune-0-1")
    assert item == expected_item

    expected_item = {
        "model": "randomforestclassifier",
        "f_score": 76,
        "features": "AU, CF, LC",
        "tuned_parameters": "n_estimators:40, max_depth:3",
    }
    item = get_model_item("randomforestclassifier-76-au-cf-lc-tune-40-3")
    assert item == expected_item
