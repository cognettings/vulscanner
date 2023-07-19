from dataclasses import (
    dataclass,
)
from dynamo_etl_conf import (
    centralize,
    jobs_sdk,
)
from dynamo_etl_conf._core import (
    TargetTables,
)
from enum import (
    Enum,
)
from fa_purity.cmd import (
    Cmd,
)
import os
from redshift_client.id_objs import (
    SchemaId,
)
from redshift_client.schema.client import (
    SchemaClient,
)


class Job(Enum):
    PHASE_1 = "PHASE_1"
    PHASE_2 = "PHASE_2"
    PHASE_3 = "PHASE_3"
    PHASE_4 = "PHASE_4"
    DETERMINE_SCHEMA = "DETERMINE_SCHEMA"


LOADING_SCHEMA = SchemaId("dynamodb_integrates_vms_merged_parts_loading")
TARGET_SCHEMA = SchemaId("dynamodb")
CACHE_URI = "s3://observes.cache/dynamoEtl/vms_schema"


@dataclass(frozen=True)
class Executor:
    schema_client: Cmd[SchemaClient]

    @staticmethod
    def phase_1() -> Cmd[None]:
        "dynamo to s3 ETL"
        return jobs_sdk.parallel_phase_1(
            240,  # total_segments: MUST coincide with batch parallel conf
            "auto",
        )

    @staticmethod
    def phase_2() -> Cmd[None]:
        "prepare loading schema"
        return centralize.prepare_loading(CACHE_URI, LOADING_SCHEMA)

    @staticmethod
    def phase_3() -> Cmd[None]:
        "s3 to redshift loading schema"
        return jobs_sdk.parallel_phase_3("auto")

    def phase_4(self) -> Cmd[None]:
        "migrate new data (at loading schema) into final schema"
        return self.schema_client.bind(
            lambda c: centralize.centralize(c, LOADING_SCHEMA, TARGET_SCHEMA)
        )

    @staticmethod
    def determine_schema() -> Cmd[None]:
        return jobs_sdk.determine_schema(
            frozenset([TargetTables.CORE.value]),
            1000,
            100,
            "s3://observes.cache/dynamoEtl/vms_schema",
        )

    def run_job(self, job: Job) -> Cmd[None]:
        if job is Job.PHASE_1:
            return self.phase_1()
        if job is Job.PHASE_2:
            return self.phase_2()
        if job is Job.PHASE_3:
            return self.phase_3()
        if job is Job.PHASE_4:
            return self.phase_4()
        if job is Job.DETERMINE_SCHEMA:
            return self.determine_schema()
