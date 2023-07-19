from cvss import (
    CVSS3,
    CVSS3Error,
)
from utils.logs import (
    log_blocking,
)


def set_default_temporal_scores(cvss_vector: str | None) -> str | None:
    if cvss_vector:
        metrics = cvss_vector.split("/")

        if first_match := next(
            (met for met in metrics if met.startswith("E:")), None
        ):
            metrics[metrics.index(first_match)] = "E:U"
        else:
            metrics.append("E:U")

        if not any(met for met in metrics if met.startswith("RL:")):
            metrics.append("RL:O")

        if not any(met for met in metrics if met.startswith("RC:")):
            metrics.append("RC:C")

        return "/".join(metrics)
    return None


def max_cvss_list(target: list) -> str | None:
    if target:
        try:
            scores = [CVSS3(elem).temporal_score for elem in target]
            return target[max(range(len(scores)), key=scores.__getitem__)]
        except CVSS3Error:
            log_blocking(
                "error",
                "Could not generate the CVSS3 score",
            )
    return None
