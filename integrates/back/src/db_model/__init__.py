from context import (
    FI_INTEGRATES_DB_MODEL_PATH,
)
from dynamodb.tables import (
    load_tables,
)
import json

with open(FI_INTEGRATES_DB_MODEL_PATH, mode="r", encoding="utf-8") as file:
    TABLE = load_tables(json.load(file))[0]
