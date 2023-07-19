import json
import requests


def handle(event, _context):
    # _context is not used
    del _context
    if event["source"] != "aws.batch":
        raise ValueError(
            "Function only supports input from events with a source type of: aws.batch"
        )
    if event["detail"]["status"] == "SUCCEEDED":
        for variable in event["detail"]["container"]["environment"]:
            if (
                variable["name"] == "BETTERSTACK_CALL_URL"
                and variable["value"]
            ):
                requests.get(variable["value"])
                return json.dumps({"message": "health updated"})

    return json.dumps({"message": "not required"})
