import boto3
from sagemaker.tuner import (
    CategoricalParameter,
    ContinuousParameter,
    IntegerParameter,
)
from sklearn.ensemble import (
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sorts.typings import (
    Model as ModelType,
)
from typing import (
    Dict,
    List,
    Union,
)
from xgboost import (
    XGBClassifier,
)

# Threshold defining the minimum elements that our dataset must have (*1000)
DATASET_THRESHOLD: int = 40

PARALLEL_JOBS = 16

# AWS-related
S3_BUCKET_NAME: str = "sorts"
S3_RESOURCE = boto3.resource("s3")
S3_BUCKET = S3_RESOURCE.Bucket(S3_BUCKET_NAME)

DATASET_PATH: str = "s3://sorts/training/binary_encoded_training_data.csv"

SAGEMAKER_METRIC_DEFINITIONS: List[Dict[str, str]] = [
    {"Name": "precision", "Regex": "Precision: (.*?)%"},
    {"Name": "recall", "Regex": "Recall: (.*?)%"},
    {"Name": "fscore", "Regex": "F1-Score: (.*?)%"},
    {"Name": "accuracy", "Regex": "Accuracy: (.*?)%"},
    {"Name": "overfit", "Regex": "Overfit: (.*?)%"},
]

# Model-related
FEATURES_DICTS: Dict[str, str] = {
    "num_commits": "CM",
    "num_unique_authors": "AU",
    "file_age": "FA",
    "midnight_commits": "MC",
    "risky_commits": "RC",
    "seldom_contributors": "SC",
    "num_lines": "LC",
    "busy_file": "BF",
    "commit_frequency": "CF",
}
RESULT_HEADERS: List[str] = [
    "Model",
    "Features",
    "Precision",
    "Recall",
    "F1",
    "Accuracy",
    "Overfit",
    "TunedParams",
    "Time",
]
MODELS: Dict[str, ModelType] = {
    "gradientboostingclassifier": GradientBoostingClassifier,
    "histgradientboostingclassifier": HistGradientBoostingClassifier,
    "randomforestclassifier": RandomForestClassifier,
    "xgbclassifier": XGBClassifier,
}
MODELS_DEFAULTS: Dict[ModelType, Dict[str, Union[str, int, float]]] = {
    GradientBoostingClassifier: {
        "n_estimators": 50,
        "learning_rate": 0.75,
    },
    RandomForestClassifier: {
        "n_estimators": 40,
        "max_depth": 32,
    },
    XGBClassifier: {
        "learning_rate": 0.1,
        "max_depth": 3,
        "subsample": 0.5,
    },
}

# Hyperparameters
MODEL_HYPERPARAMETERS = {
    "gradientboostingclassifier": {
        "n_estimators": IntegerParameter(20, 150, scaling_type="Logarithmic"),
        "learning_rate": ContinuousParameter(
            0.01, 0.7, scaling_type="Logarithmic"
        ),
    },
    "histgradientboostingclassifier": {
        "max_leaf_nodes": CategoricalParameter([0, 5, 25, 50, 100, 250, 500]),
        "learning_rate": ContinuousParameter(
            0.01, 1, scaling_type="Logarithmic"
        ),
    },
    "randomforestclassifier": {
        "n_estimators": IntegerParameter(40, 70),
        "max_depth": IntegerParameter(3, 32),
    },
    "xgbclassifier": {
        "learning_rate": ContinuousParameter(
            0.01, 0.2, scaling_type="Logarithmic"
        ),
        "max_depth": IntegerParameter(3, 7),
        "min_child_weight": IntegerParameter(3, 7),
    },
}
