# pylint: disable=too-many-lines
# pylint: disable=invalid-name
from __future__ import (
    annotations,
)

from enum import (
    Enum,
)
import hashlib
from model.utils.what import (
    format_what,
    get_apk_details,
    get_missing_dependency,
)
import re
from typing import (
    NamedTuple,
)


class Platform(Enum):
    COMPOSER: str = "COMPOSER"
    CONAN: str = "CONAN"
    PIP: str = "PIP"
    NPM: str = "NPM"
    MAVEN: str = "MAVEN"
    NUGET: str = "NUGET"
    GEM: str = "GEM"
    GO: str = "GO"
    PUB: str = "PUB"


class DependenciesTypeEnum(Enum):
    DEV: str = "devDependencies"
    PROD: str = "dependencies"


class AvailabilityEnum(Enum):
    ALWAYS = "ALWAYS"
    WORKING_HOURS = "WORKING_HOURS"
    NEVER = "NEVER"


class ExecutionQueueConfig(NamedTuple):
    availability: AvailabilityEnum
    name: str


class ExecutionQueue(Enum):
    dast = ExecutionQueueConfig(
        availability=AvailabilityEnum.WORKING_HOURS, name="dast"
    )
    sast = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="sast"
    )
    sca = ExecutionQueueConfig(
        availability=AvailabilityEnum.ALWAYS, name="sca"
    )


class FindingMetadata(NamedTuple):
    auto_approve: bool
    cwe: str  # must have the format CWE-{number}, ex CWE-139
    description: str
    execution_queue: ExecutionQueue
    impact: str
    recommendation: str
    requirements: list[int]
    threat: str
    title: str

    @classmethod
    def new(
        cls,
        *,
        code: str,
        cwe: str,
        execution_queue: ExecutionQueue,
        auto_approve: bool,
        requirements: list[int],
    ) -> FindingMetadata:
        return FindingMetadata(
            auto_approve=auto_approve,
            cwe=cwe,
            description=f"criteria.vulns.{code[1:]}.description",
            execution_queue=execution_queue,
            impact=f"criteria.vulns.{code[1:]}.impact",
            recommendation=f"criteria.vulns.{code[1:]}.recommendation",
            requirements=requirements,
            threat=f"criteria.vulns.{code[1:]}.threat",
            title=f"criteria.vulns.{code[1:]}.title",
        )


class FindingEnum(Enum):
    F001: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F001",
        cwe="CWE-89",
        execution_queue=ExecutionQueue.sast,
        requirements=[169],
    )
    F004: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F004",
        cwe="CWE-78",
        execution_queue=ExecutionQueue.sast,
        requirements=[173, 265],
    )
    F005: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F004",
        cwe="CWE-78",
        execution_queue=ExecutionQueue.sast,
        requirements=[35],
    )
    F007: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F007",
        cwe="CWE-352",
        execution_queue=ExecutionQueue.sast,
        requirements=[29, 174],
    )
    F008: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F008",
        cwe="CWE-79",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F009: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F009",
        cwe="CWE-798",
        execution_queue=ExecutionQueue.sast,
        requirements=[156],
    )
    F011: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F011",
        cwe="CWE-937",
        execution_queue=ExecutionQueue.sca,
        requirements=[262],
    )
    F012: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F012",
        cwe="CWE-89",
        execution_queue=ExecutionQueue.sast,
        requirements=[169],
    )
    F015: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F015",
        cwe="CWE-287",
        execution_queue=ExecutionQueue.dast,
        requirements=[228, 319],
    )
    F016: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F016",
        cwe="CWE-326",
        execution_queue=ExecutionQueue.dast,
        requirements=[148, 149, 150, 181, 336],
    )
    F017: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F017",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.sast,
        requirements=[32, 181],
    )
    F021: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F021",
        cwe="CWE-643",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F022: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F022",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.sast,
        requirements=[181],
    )
    F023: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F023",
        cwe="CWE-601",
        execution_queue=ExecutionQueue.dast,
        requirements=[173, 324],
    )
    F024: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F024",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[255, 266],
    )
    F031: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F031",
        cwe="CWE-250",
        execution_queue=ExecutionQueue.sast,
        requirements=[186],
    )
    F034: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F034",
        cwe="CWE-330",
        execution_queue=ExecutionQueue.sast,
        requirements=[223, 224],
    )
    F035: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F035",
        cwe="CWE-521",
        execution_queue=ExecutionQueue.sast,
        requirements=[130, 132, 133, 139, 332],
    )
    F036: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F036",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.dast,
        requirements=[26],
    )
    F037: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F037",
        cwe="CWE-200",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 176],
    )
    F042: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F042",
        cwe="CWE-614",
        execution_queue=ExecutionQueue.sast,
        requirements=[29],
    )
    F043: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F043",
        cwe="CWE-644",
        execution_queue=ExecutionQueue.dast,
        requirements=[62],
    )
    F044: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F044",
        cwe="CWE-650",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F046: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F046",
        cwe="CWE-1269",
        execution_queue=ExecutionQueue.sast,
        requirements=[159],
    )
    F048: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F048",
        cwe="CWE-250",
        execution_queue=ExecutionQueue.sast,
        requirements=[326],
    )
    F052: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F052",
        cwe="CWE-310",
        execution_queue=ExecutionQueue.dast,
        requirements=[158, 149, 150, 181, 336],
    )
    F055: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F055",
        cwe="CWE-530",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F056: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F056",
        cwe="CWE-284",
        execution_queue=ExecutionQueue.sast,
        requirements=[142, 264, 265, 266, 319],
    )
    F058: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F058",
        cwe="CWE-489",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 78],
    )
    F059: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F059",
        cwe="CWE-209",
        execution_queue=ExecutionQueue.sast,
        requirements=[83],
    )
    F060: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F060",
        cwe="CWE-396",
        execution_queue=ExecutionQueue.sast,
        requirements=[359],
    )
    F063: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F063",
        cwe="CWE-22",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F064: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F064",
        cwe="CWE-778",
        execution_queue=ExecutionQueue.dast,
        requirements=[75],
    )
    F065: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F065",
        cwe="CWE-200",
        execution_queue=ExecutionQueue.sast,
        requirements=[177],
    )
    F066: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F066",
        cwe="CWE-200",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 176],
    )
    F070: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F070",
        cwe="CWE-266",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F071: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F071",
        cwe="CWE-644",
        execution_queue=ExecutionQueue.dast,
        requirements=[62],
    )
    F073: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F073",
        cwe="CWE-478",
        execution_queue=ExecutionQueue.sast,
        requirements=[161],
    )
    F075: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F075",
        cwe="CWE-284",
        execution_queue=ExecutionQueue.sast,
        requirements=[176],
    )
    F079: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F079",
        cwe="CWE-829",
        execution_queue=ExecutionQueue.sast,
        requirements=[302],
    )
    F081: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F081",
        cwe="CWE-308",
        execution_queue=ExecutionQueue.sast,
        requirements=[229, 231, 264, 319, 328],
    )
    F082: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F082",
        cwe="CWE-459",
        execution_queue=ExecutionQueue.sast,
        requirements=[183],
    )
    F083: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F083",
        cwe="CWE-611",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F085: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F085",
        cwe="CWE-922",
        execution_queue=ExecutionQueue.sast,
        requirements=[329],
    )
    F086: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F086",
        cwe="CWE-353",
        execution_queue=ExecutionQueue.dast,
        requirements=[178, 262, 330],
    )
    F089: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F089",
        cwe="CWE-501",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F091: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F091",
        cwe="CWE-117",
        execution_queue=ExecutionQueue.sast,
        requirements=[80, 173],
    )
    F094: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F094",
        cwe="CWE-757",
        execution_queue=ExecutionQueue.dast,
        requirements=[148, 149, 150, 181, 336],
    )
    F096: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F096",
        cwe="CWE-502",
        execution_queue=ExecutionQueue.sast,
        requirements=[173, 321],
    )
    F097: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F097",
        cwe="CWE-502",
        execution_queue=ExecutionQueue.sast,
        requirements=[173, 324],
    )
    F098: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F098",
        cwe="CWE-22",
        execution_queue=ExecutionQueue.sast,
        requirements=[29, 173],
    )
    F099: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F099",
        cwe="CWE-311",
        execution_queue=ExecutionQueue.sast,
        requirements=[134, 135, 185, 227, 229, 264, 300],
    )
    F100: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F100",
        cwe="CWE-918",
        execution_queue=ExecutionQueue.sast,
        requirements=[173, 324],
    )
    F101: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F101",
        cwe="CWE-693",
        execution_queue=ExecutionQueue.sast,
        requirements=[186, 265],
    )
    F103: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F103",
        cwe="CWE-325",
        execution_queue=ExecutionQueue.sast,
        requirements=[178],
    )
    F107: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F107",
        cwe="CWE-90",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F109: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F109",
        cwe="CWE-681",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F112: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F112",
        cwe="CWE-89",
        execution_queue=ExecutionQueue.sast,
        requirements=[169],
    )
    F117: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F117",
        cwe="CWE-377",
        execution_queue=ExecutionQueue.sast,
        requirements=[323],
    )
    F120: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F120",
        cwe="CWE-829",
        execution_queue=ExecutionQueue.sca,
        requirements=[302],
    )
    F127: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F127",
        cwe="CWE-843",
        execution_queue=ExecutionQueue.sast,
        requirements=[342],
    )
    F128: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F128",
        cwe="CWE-1004",
        execution_queue=ExecutionQueue.dast,
        requirements=[29],
    )
    F129: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F129",
        cwe="CWE-1275",
        execution_queue=ExecutionQueue.dast,
        requirements=[29],
    )
    F130: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F130",
        cwe="CWE-614",
        execution_queue=ExecutionQueue.dast,
        requirements=[29],
    )
    F131: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F131",
        cwe="CWE-644",
        execution_queue=ExecutionQueue.dast,
        requirements=[62, 181],
    )
    F132: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F132",
        cwe="CWE-644",
        execution_queue=ExecutionQueue.dast,
        requirements=[62],
    )
    F133: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F133",
        cwe="CWE-310",
        execution_queue=ExecutionQueue.dast,
        requirements=[148, 149, 150, 181],
    )
    F134: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F134",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[62, 266, 349],
    )
    F135: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F135",
        cwe="CWE-644",
        execution_queue=ExecutionQueue.sast,
        requirements=[62, 175, 266, 349],
    )
    F143: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F143",
        cwe="CWE-676",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F148: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F148",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.sast,
        requirements=[181],
    )
    F149: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F149",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.sast,
        requirements=[181],
    )
    F152: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F152",
        cwe="CWE-693",
        execution_queue=ExecutionQueue.sast,
        requirements=[62, 175, 266, 349],
    )
    F153: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F153",
        cwe="CWE-644",
        execution_queue=ExecutionQueue.sast,
        requirements=[62, 266, 349],
    )
    F157: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F157",
        cwe="CWE-923",
        execution_queue=ExecutionQueue.sast,
        requirements=[255],
    )
    F160: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F160",
        cwe="CWE-378",
        execution_queue=ExecutionQueue.sast,
        requirements=[95, 96, 186],
    )
    F164: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F164",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[185, 266],
    )
    F165: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F165",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[185, 265, 266],
    )
    F169: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F169",
        cwe="CWE-798",
        execution_queue=ExecutionQueue.sast,
        requirements=[145],
    )
    F176: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F176",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F177: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F177",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F182: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F182",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.dast,
        requirements=[62, 273],
    )
    F183: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F183",
        cwe="CWE-489",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 78],
    )
    F188: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F188",
        cwe="CWE-489",
        execution_queue=ExecutionQueue.sast,
        requirements=[173, 320, 342],
    )
    F200: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F200",
        cwe="CWE-778",
        execution_queue=ExecutionQueue.sast,
        requirements=[75, 320],
    )
    F203: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F203",
        cwe="CWE-284",
        execution_queue=ExecutionQueue.sast,
        requirements=[96, 176, 264, 320],
    )
    F206: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F206",
        cwe="CWE-295",
        execution_queue=ExecutionQueue.sast,
        requirements=[62, 266, 273],
    )
    F207: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F207",
        cwe="CWE-295",
        execution_queue=ExecutionQueue.sast,
        requirements=[93],
    )
    F211: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F211",
        cwe="CWE-405",
        execution_queue=ExecutionQueue.sast,
        requirements=[72],
    )
    F234: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F234",
        cwe="CWE-209",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 176],
    )
    F236: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F236",
        cwe="CWE-200",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 176],
    )
    F237: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F237",
        cwe="CWE-200",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 176],
    )
    F239: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F239",
        cwe="CWE-200",
        execution_queue=ExecutionQueue.sast,
        requirements=[77, 176],
    )
    F246: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F246",
        cwe="CWE-311",
        execution_queue=ExecutionQueue.sast,
        requirements=[134, 135, 185, 229, 264, 300],
    )
    F250: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F250",
        cwe="CWE-313",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F256: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F256",
        cwe="CWE-693",
        execution_queue=ExecutionQueue.sast,
        requirements=[186, 265],
    )
    F257: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F257",
        cwe="CWE-463",
        execution_queue=ExecutionQueue.sast,
        requirements=[186, 265],
    )
    F258: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F258",
        cwe="CWE-463",
        execution_queue=ExecutionQueue.sast,
        requirements=[186, 265],
    )
    F259: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F259",
        cwe="CWE-463",
        execution_queue=ExecutionQueue.sast,
        requirements=[186, 265],
    )
    F266: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F266",
        cwe="CWE-250",
        execution_queue=ExecutionQueue.sast,
        requirements=[95, 96, 186],
    )
    F267: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F267",
        cwe="CWE-250",
        execution_queue=ExecutionQueue.sast,
        requirements=[95, 186],
    )
    F268: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F268",
        cwe="CWE-749",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F277: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F277",
        cwe="CWE-521",
        execution_queue=ExecutionQueue.sast,
        requirements=[130, 132, 133, 139, 332],
    )
    F280: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F280",
        cwe="CWE-384",
        execution_queue=ExecutionQueue.sast,
        requirements=[30],
    )
    F281: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F281",
        cwe="CWE-311",
        execution_queue=ExecutionQueue.sast,
        requirements=[181],
    )
    F297: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F297",
        cwe="CWE-89",
        execution_queue=ExecutionQueue.sast,
        requirements=[169, 173],
    )
    F300: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F300",
        cwe="CWE-284",
        execution_queue=ExecutionQueue.sast,
        requirements=[227, 228, 229, 231, 235, 264, 323],
    )
    F309: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F309",
        cwe="CWE-287",
        execution_queue=ExecutionQueue.sast,
        requirements=[228],
    )
    F313: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F313",
        cwe="CWE-295",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F320: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F320",
        cwe="CWE-90",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F325: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F325",
        cwe="CWE-250",
        execution_queue=ExecutionQueue.sast,
        requirements=[95, 96, 186],
    )
    F332: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F332",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.sast,
        requirements=[181],
    )
    F333: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F333",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F335: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F335",
        cwe="CWE-922",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F338: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F338",
        cwe="CWE-749",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F343: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F343",
        cwe="CWE-444",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F344: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F344",
        cwe="CWE-922",
        execution_queue=ExecutionQueue.sast,
        requirements=[173, 320, 357],
    )
    F346: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F346",
        cwe="CWE-272",
        execution_queue=ExecutionQueue.sast,
        requirements=[95, 96, 186],
    )
    F350: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F350",
        cwe="CWE-310",
        execution_queue=ExecutionQueue.sast,
        requirements=[88, 89, 90, 91, 92, 93],
    )
    F353: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F353",
        cwe="CWE-287",
        execution_queue=ExecutionQueue.sast,
        requirements=[228],
    )
    F354: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F354",
        cwe="CWE-770",
        execution_queue=ExecutionQueue.sast,
        requirements=[40, 41],
    )
    F358: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F358",
        cwe="CWE-295",
        execution_queue=ExecutionQueue.sast,
        requirements=[158],
    )
    F363: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F363",
        cwe="CWE-521",
        execution_queue=ExecutionQueue.sast,
        requirements=[130, 132, 133, 139, 332],
    )
    F366: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F366",
        cwe="CWE-749",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F368: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F368",
        cwe="CWE-923",
        execution_queue=ExecutionQueue.sast,
        requirements=[255],
    )
    F371: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F371",
        cwe="CWE-79",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F372: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F372",
        cwe="CWE-650",
        execution_queue=ExecutionQueue.sast,
        requirements=[181],
    )
    F379: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F379",
        cwe="CWE-650",
        execution_queue=ExecutionQueue.sast,
        requirements=[158],
    )
    F380: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F380",
        cwe="CWE-749",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F381: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F381",
        cwe="CWE-437",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F393: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F393",
        cwe="CWE-937",
        execution_queue=ExecutionQueue.sca,
        requirements=[48, 262],
    )
    F394: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F394",
        cwe="CWE-117",
        execution_queue=ExecutionQueue.sast,
        requirements=[80],
    )
    F396: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F396",
        cwe="CWE-255",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F398: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F398",
        cwe="CWE-470",
        execution_queue=ExecutionQueue.sast,
        requirements=[266, 173],
    )
    F400: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F400",
        cwe="CWE-778",
        execution_queue=ExecutionQueue.sast,
        requirements=[75, 376, 377, 378],
    )
    F401: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F401",
        cwe="CWE-521",
        execution_queue=ExecutionQueue.sast,
        requirements=[130, 138, 140],
    )
    F402: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F402",
        cwe="CWE-778",
        execution_queue=ExecutionQueue.sast,
        requirements=[75, 376, 377, 378],
    )
    F403: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F403",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.sast,
        requirements=[130, 138, 140],
    )
    F405: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F405",
        cwe="CWE-732",
        execution_queue=ExecutionQueue.sast,
        requirements=[33, 176, 265, 280],
    )
    F406: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F406",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[185, 265, 266],
    )
    F407: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F407",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[185, 265, 266],
    )
    F408: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F408",
        cwe="CWE-778",
        execution_queue=ExecutionQueue.sast,
        requirements=[75, 376, 377, 378],
    )
    F411: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F411",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[147, 151, 181, 224],
    )
    F412: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F412",
        cwe="CWE-463",
        execution_queue=ExecutionQueue.sast,
        requirements=[186, 265],
    )
    F413: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F413",
        cwe="CWE-434",
        execution_queue=ExecutionQueue.sast,
        requirements=[40, 41],
    )
    F414: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F414",
        cwe="CWE-644",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F416: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F416",
        cwe="CWE-94",
        execution_queue=ExecutionQueue.sast,
        requirements=[173],
    )
    F418: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F418",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F423: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F423",
        cwe="CWE-382",
        execution_queue=ExecutionQueue.sast,
        requirements=[164, 167, 72, 327],
    )
    F426: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F426",
        cwe="CWE-749",
        execution_queue=ExecutionQueue.sast,
        requirements=[266],
    )
    F427: FindingMetadata = FindingMetadata.new(
        auto_approve=True,
        code="F427",
        cwe="CWE-319",
        execution_queue=ExecutionQueue.sast,
        requirements=[181],
    )
    F433: FindingMetadata = FindingMetadata.new(
        auto_approve=False,
        code="F433",
        cwe="CWE-16",
        execution_queue=ExecutionQueue.sast,
        requirements=[185, 300],
    )


FINDING_ENUM_FROM_STR: dict[str, FindingEnum] = {
    __finding.name: __finding for __finding in FindingEnum
}


class VulnerabilityStateEnum(Enum):
    OPEN: str = "open"
    CLOSED: str = "closed"


class VulnerabilityKindEnum(Enum):
    CSPM: str = "CSPM"
    DAST: str = "DAST"
    SAST: str = "SAST"
    SCA: str = "SCA"


class GrammarMatch(NamedTuple):
    start_column: int
    start_line: int


class SkimsAPKConfig(NamedTuple):
    exclude: tuple[str, ...]
    include: tuple[str, ...]


class SkimsHttpConfig(NamedTuple):
    include: tuple[str, ...]


class SkimsSastConfig(NamedTuple):
    exclude: tuple[str, ...]
    include: tuple[str, ...]
    lib_path: bool
    lib_root: bool
    recursion_limit: int | None


class SkimsScaConfig(NamedTuple):
    exclude: tuple[str, ...]
    include: tuple[str, ...]


class SkimsSslTarget(NamedTuple):
    host: str
    port: int


class SkimsSslConfig(NamedTuple):
    include: tuple[SkimsSslTarget, ...]


class SkimsDastConfig(NamedTuple):
    aws_credentials: list[AwsCredentials | None]
    urls: tuple[str, ...]
    http_checks: bool
    ssl_checks: bool


class OutputFormat(Enum):
    CSV: str = "CSV"
    SARIF: str = "SARIF"


class SkimsOutputConfig(NamedTuple):
    file_path: str
    format: OutputFormat


class AwsCredentials(NamedTuple):
    access_key_id: str
    secret_access_key: str


class LocalesEnum(Enum):
    EN: str = "EN"
    ES: str = "ES"


class SkimsConfig(NamedTuple):
    sast: SkimsSastConfig
    sca: SkimsScaConfig
    apk: SkimsAPKConfig
    debug: bool
    checks: set[FindingEnum]
    language: LocalesEnum
    multifile: bool
    namespace: str
    strict: bool
    output: SkimsOutputConfig | None
    start_dir: str
    working_dir: str
    dast: SkimsDastConfig | None
    execution_id: str | None
    commit: str | None


class HTTPProperties(NamedTuple):
    has_redirect: bool
    original_url: str


class SkimsVulnerabilityMetadata(NamedTuple):
    cwe_ids: list[str]
    cve: list[str] | None
    vulnerable_version: str | None
    package: str | None
    cvss: str | None
    description: str
    http_properties: HTTPProperties | None
    snippet: str
    source_method: str
    developer: DeveloperEnum
    technique: TechniqueEnum


class Vulnerability(NamedTuple):
    finding: FindingEnum
    kind: VulnerabilityKindEnum
    namespace: str
    skims_metadata: SkimsVulnerabilityMetadata
    state: VulnerabilityStateEnum
    what: str
    where: str

    stream: str | None = "skims"

    @property
    def digest(self) -> int:
        """Hash a Vulnerability according to Integrates rules."""
        location = format_what(self)
        specific = self.where
        method = self.skims_metadata.source_method
        extra_info: str | None = ""
        # if you want to add a field to the hash you must
        # also do it in the integrates function
        if (
            self.skims_metadata.source_method
            == "python.pip_incomplete_dependencies_list"
        ):
            extra_info = (get_missing_dependency(location) or {}).get(
                "dependency_name"
            )
        elif self.skims_metadata.technique == TechniqueEnum.APK and (
            details := (get_apk_details(location) or {}).get("details")
        ):
            extra_info = details

        return int.from_bytes(
            hashlib.sha256(
                bytes(
                    (
                        location
                        + specific
                        + self.finding.value.title.split(".")[2]
                        + method
                        + (extra_info or "")
                    ),
                    "utf-8",
                )
            ).digest()[:8],
            "little",
        )

    @property
    def digest_future(self) -> int:
        """Hash a Vulnerability according to Integrates rules."""
        location = format_what(self)
        specific = self.where
        method = self.skims_metadata.source_method
        extra_info: str | None = ""
        vulnerable_version = self.skims_metadata.vulnerable_version
        package = self.skims_metadata.package
        # if you want to add a field to the hash you must
        # also do it in the integrates function
        if (
            self.skims_metadata.source_method
            == "python.pip_incomplete_dependencies_list"
        ):
            extra_info = (get_missing_dependency(location) or {}).get(
                "dependency_name"
            )
        elif self.skims_metadata.technique == TechniqueEnum.APK and (
            details := (get_apk_details(location) or {}).get("details")
        ):
            extra_info = details

        return int.from_bytes(
            hashlib.sha256(
                bytes(
                    (
                        location
                        + specific
                        + self.finding.value.title.split(".")[2]
                        + method
                        + (extra_info or "")
                        + (package or "")
                        + (vulnerable_version or "")
                    ),
                    "utf-8",
                )
            ).digest()[:8],
            "little",
        )

    @property
    def what_on_integrates(self) -> str:
        what = re.sub(r"\s(\(.*?\))((\s)(\[.*?\]))?", "", self.what)  # NOSONAR
        while what.endswith("/"):
            what = what.rstrip("/")
        return what


Vulnerabilities = tuple[Vulnerability, ...]


class DeveloperEnum(Enum):
    ALEJANDRO_SALGADO: str = "asalgado@fluidattacks.com"
    ALEJANDRO_TRUJILLO: str = "atrujillo@fluidattacks.com"
    ANDRES_CUBEROS: str = "acuberos@fluidattacks.com"
    BRIAM_AGUDELO: str = "bagudelo@fluidattacks.com"
    DEFAULT: str = "machine@fluidattacks.com"
    DIEGO_RESTREPO: str = "drestrepo@fluidattacks.com"
    FABIO_LAGOS: str = "flagos@fluidattacks.com"
    FLOR_CALDERON: str = "fcalderon@fluidattacks.com"
    JUAN_ECHEVERRI: str = "jecheverri@fluidattacks.com"
    LEWIS_CONTRERAS: str = "lcontreras@fluidattacks.com"
    LUIS_SAAVEDRA: str = "lsaavedra@fluidattacks.com"
    JULIAN_GOMEZ: str = "ugomez@fluidattacks.com"
    JHON_ROMERO: str = "jromero@fluidattacks.com"
    LUIS_PATINO: str = "lpatino@fluidattacks.com"


class TechniqueEnum(Enum):
    APK: str = "APK"
    SCA: str = "SCA"
    ADVANCE_SAST: str = "ASAST"
    BASIC_SAST: str = "BSAST"
    DAST: str = "DAST"


class MethodOriginEnum(Enum):
    ARM: str = "ARM"
    ASSERTS: str = "ASSERTS"
    DEVELOPER: str = "DEVELOPER"
    HACKER: str = "HACKER"
    EXTERNAL: str = "EXTERNAL"


class MethodInfo(NamedTuple):
    file_name: str
    name: str
    module: str
    finding: FindingEnum
    developer: DeveloperEnum
    technique: TechniqueEnum
    origin: MethodOriginEnum
    cvss: str | None = None
    cwe_ids: list[str] | None = None

    def get_name(self) -> str:
        return f"{self.file_name}.{self.name}"

    def get_cwe(self) -> list[str]:
        return self.cwe_ids if self.cwe_ids else [self.finding.value.cwe]

    def get_finding(self) -> str:
        return self.finding.name.replace("F", "")


class MethodsEnum(Enum):
    CS_SQL_INJECTION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_sql_injection",
        module="lib/root",
        finding=FindingEnum.F001,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-89"],
    )
    CS_UNSAFE_SQL_STATEMENT = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_sql_user_params",
        module="lib/root",
        finding=FindingEnum.F001,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-89"],
    )
    CS_REMOTE_COMMAND_EXECUTION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_remote_command_execution",
        module="lib/root",
        finding=FindingEnum.F004,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:P/RL:T/RC:R",
        cwe_ids=["CWE-78"],
    )
    JAVA_REMOTE_COMMAND_EXECUTION = MethodInfo(
        file_name="java",
        name="java_remote_command_execution",
        module="lib/root",
        finding=FindingEnum.F004,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:P/RL:T/RC:R",
        cwe_ids=["CWE-78"],
    )
    JS_REMOTE_COMMAND_EXECUTION = MethodInfo(
        file_name="javascript",
        name="javascript_remote_command_execution",
        module="lib/root",
        finding=FindingEnum.F004,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:P/RL:T/RC:R",
        cwe_ids=["CWE-78"],
    )
    TS_REMOTE_COMMAND_EXECUTION = MethodInfo(
        file_name="typescript",
        name="typescript_remote_command_execution",
        module="lib/root",
        finding=FindingEnum.F004,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:P/RL:T/RC:R",
        cwe_ids=["CWE-78"],
    )
    KT_REMOTE_COMMAND_EXECUTION = MethodInfo(
        file_name="kotlin",
        name="kt_remote_command_execution",
        module="lib/root",
        finding=FindingEnum.F004,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:P/RL:T/RC:R",
        cwe_ids=["CWE-78"],
    )
    PYTHON_REMOTE_COMMAND_EXECUTION = MethodInfo(
        file_name="python",
        name="python_remote_command_execution",
        module="lib/root",
        finding=FindingEnum.F004,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H/E:P/RL:T/RC:R",
        cwe_ids=["CWE-78"],
    )
    AWS_ALLOWS_PRIV_ESCALATION_BY_POLICIES_VERSIONS = MethodInfo(
        file_name="aws",
        name="allows_priv_escalation_by_policies_versions",
        module="lib/dast",
        finding=FindingEnum.F005,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ALLOWS_PRIV_ESCALATION_BY_ATTACH_POLICY = MethodInfo(
        file_name="aws",
        name="allows_priv_escalation_by_attach_policy",
        module="lib/dast",
        finding=FindingEnum.F005,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_CSRF_PROTECTIONS_DISABLED = MethodInfo(
        file_name="java",
        name="csrf_protections_disabled",
        module="lib/root",
        finding=FindingEnum.F007,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:P/RL:X/RC:R",
        cwe_ids=["CWE-352"],
    )
    CS_INSEC_ADDHEADER_WRITE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insec_addheader_write",
        module="lib/root",
        finding=FindingEnum.F008,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:X/RL:X/RC:X",
        cwe_ids=["CWE-79"],
    )
    JAVA_UNSAFE_XSS_CONTENT = MethodInfo(
        file_name="java",
        name="java_unsafe_xss_content",
        module="lib/root",
        finding=FindingEnum.F008,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:P/RL:X/RC:R",
        cwe_ids=["CWE-79"],
    )
    JS_UNSAFE_XSS_CONTENT = MethodInfo(
        file_name="javascript",
        name="javascript_unsafe_xss_content",
        module="lib/root",
        finding=FindingEnum.F008,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:P/RL:X/RC:R",
        cwe_ids=["CWE-79"],
    )
    TS_UNSAFE_XSS_CONTENT = MethodInfo(
        file_name="typescript",
        name="typescript_unsafe_xss_content",
        module="lib/root",
        finding=FindingEnum.F008,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:P/RL:X/RC:R",
        cwe_ids=["CWE-79"],
    )
    AWS_CREDENTIALS = MethodInfo(
        file_name="aws",
        name="aws_credentials",
        module="lib/path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    DOCKER_ENV_SECRETS = MethodInfo(
        file_name="docker",
        name="dockerfile_env_secrets",
        module="lib/path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    DOCKER_COMPOSE_ENV_SECRETS = MethodInfo(
        file_name="docker_compose",
        name="docker_compose_env_secrets",
        module="lib/root",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    JAVA_PROP_SENSITIVE = MethodInfo(
        file_name="java",
        name="java_properties_sensitive_data",
        module="lib/path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    SENSITIVE_KEY_JSON = MethodInfo(
        file_name="conf_files",
        name="sensitive_key_in_json",
        module="lib/root",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    SENSITIVE_INFO_DOTNET_JSON = MethodInfo(
        file_name="conf_files",
        name="sensitive_info_in_dotnet_json",
        module="lib/root",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    SENSITIVE_INFO_JSON = MethodInfo(
        file_name="conf_files",
        name="sensitive_info_in_json",
        module="lib/root",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    WEB_USER_PASS = MethodInfo(
        file_name="conf_files",
        name="web_config_user_pass",
        module="lib/path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    WEB_DB_CONN = MethodInfo(
        file_name="conf_files",
        name="web_config_db_connection",
        module="lib/path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JS_CRYPTO_CREDENTIALS = MethodInfo(
        file_name="javascript",
        name="javascript_crypto_js_credentials",
        module="lib/root",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    TS_CRYPTO_CREDENTIALS = MethodInfo(
        file_name="typescript",
        name="typescript_crypto_ts_credentials",
        module="lib/root",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-798"],
    )
    JWT_TOKEN = MethodInfo(
        file_name="conf_files",
        name="jwt_token",
        module="lib/path",
        finding=FindingEnum.F009,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    COMPOSER_JSON = MethodInfo(
        file_name="composer",
        name="composer_json",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    COMPOSER_LOCK = MethodInfo(
        file_name="composer",
        name="composer_lock",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CONAN_LOCK = MethodInfo(
        file_name="conan",
        name="conan_lock",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CONAN_CONANFILE_PY = MethodInfo(
        file_name="python_config_files",
        name="conan_conanfile_py",
        module="lib/root",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CONAN_CONANFILE_TXT = MethodInfo(
        file_name="conan",
        name="conan_conanfile_txt",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    GEM_GEMFILE = MethodInfo(
        file_name="gem",
        name="gem_gemfile",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    GEM_GEMFILE_LOCK = MethodInfo(
        file_name="gem",
        name="gem_gemfile_lock",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    GO_MOD = MethodInfo(
        file_name="go",
        name="go_mod",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    MAVEN_POM_XML = MethodInfo(
        file_name="maven",
        name="maven_pom_xml",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    MAVEN_GRADLE = MethodInfo(
        file_name="maven",
        name="maven_gradle",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    MAVEN_SBT = MethodInfo(
        file_name="maven",
        name="maven_sbt",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    NPM_YARN_LOCK = MethodInfo(
        file_name="npm",
        name="npm_yarn_lock",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    NPM_PACKAGE_JSON = MethodInfo(
        file_name="npm",
        name="npm_package_json",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    NPM_PACKAGE_LOCK_JSON = MethodInfo(
        file_name="npm",
        name="npm_package_lock_json",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    NUGET_CSPROJ = MethodInfo(
        file_name="nuget",
        name="nuget_csproj",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    NUGET_PACKAGES_CONFIG = MethodInfo(
        file_name="nuget",
        name="nuget_packages_config",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    PIP_REQUIREMENTS_TXT = MethodInfo(
        file_name="pip",
        name="pip_requirements_txt",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    PUB_PUBSPEC_YAML = MethodInfo(
        file_name="pub",
        name="pub_pubspec_yaml",
        module="lib/sca",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CS_XSL_TRANSFORM_OBJECT = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_xsl_transform_object",
        module="lib/root",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N/E:P/RC:R",
        cwe_ids=["CWE-611"],
    )
    CS_SCHEMA_BY_URL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_schema_by_url",
        module="lib/root",
        finding=FindingEnum.F011,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:P/RC:C",
        cwe_ids=["CWE-611", "CWE-827"],
    )
    JAVA_JPA_LIKE = MethodInfo(
        file_name="java",
        name="java_jpa_like",
        module="lib/root",
        finding=FindingEnum.F012,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:P/RC:C",
        cwe_ids=["CWE-89"],
    )
    JMX_HEADER_BASIC = MethodInfo(
        file_name="conf_files",
        name="jmx_header_basic",
        module="lib/path",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    TFM_AZURE_VM_INSEC_AUTH = MethodInfo(
        file_name="terraform",
        name="tfm_azure_virtual_machine_insecure_authentication",
        module="lib/root",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-287"],
    )
    TFM_AZURE_LNX_VM_INSEC_AUTH = MethodInfo(
        file_name="terraform",
        name="tfm_azure_linux_vm_insecure_authentication",
        module="lib/root",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-287"],
    )
    WWW_AUTHENTICATE = MethodInfo(
        file_name="analyze_headers",
        name="www_authenticate",
        module="lib/http",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    XML_BASIC_AUTH_METHOD = MethodInfo(
        file_name="conf_files",
        name="xml_basic_auth_method",
        module="lib/path",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_INSECURE_AUTHENTICATION = MethodInfo(
        file_name="java",
        name="java_insecure_authentication",
        module="lib/root",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-287"],
    )
    JAVA_BASIC_AUTHENTICATION = MethodInfo(
        file_name="java",
        name="java_basic_authentication",
        module="lib/root",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-287"],
    )
    CS_INSECURE_AUTHENTICATION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_authentication",
        module="lib/root",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:H/RC:C",
        cwe_ids=["CWE-319"],
    )
    PYTHON_INSECURE_AUTHENTICATION = MethodInfo(
        file_name="python",
        name="python_insecure_authentication",
        module="lib/root",
        finding=FindingEnum.F015,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:H/RC:C",
        cwe_ids=["CWE-319"],
    )
    CS_WEAK_PROTOCOL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_weak_protocol",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-295"],
    )
    CS_SERVICE_POINT_MANAGER_DISABLED = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_service_point_manager_disabled",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-284", "CWE-285", "CWE-290"],
    )
    CS_INSECURE_SHARED_ACCESS_PROTOCOL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_shared_access_protocol",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:H/E:P/RC:R",
        cwe_ids=["CWE-311"],
    )
    CS_HTTPCLIENT_NO_REVOCATION_LIST = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_httpclient_no_revocation_list",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-311"],
    )
    KT_DEFAULT_HTTP_CLIENT_DEPRECATED = MethodInfo(
        file_name="kotlin",
        name="kt_default_http_client_deprecated",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-311"],
    )
    CFN_INSEC_PROTO = MethodInfo(
        file_name="cloudformation",
        name="cfn_serves_content_over_insecure_protocols",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-311"],
    )
    CFN_ELB_WITHOUT_SSLPOLICY = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb_without_sslpolicy",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-311"],
    )
    TFM_AWS_INSEC_PROTO = MethodInfo(
        file_name="terraform",
        name="tfm_aws_serves_content_over_insecure_protocols",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-311"],
    )
    TFM_AZURE_INSEC_PROTO = MethodInfo(
        file_name="terraform",
        name="tfm_azure_serves_content_over_insecure_protocols",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-311"],
    )
    TFM_AWS_ELB_WITHOUT_SSLPOLICY = MethodInfo(
        file_name="terraform",
        name="tfm_aws_elb_without_sslpolicy",
        module="lib/root",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-311"],
    )
    SSLV3_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="sslv3_enabled",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TLSV1_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_enabled",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TLSV1_1_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_1_enabled",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TLSV1_2_OR_HIGHER_DISABLED = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_2_or_higher_disabled",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    FALLBACK_SCSV_DISABLED = MethodInfo(
        file_name="analyze_protocol",
        name="fallback_scsv_disabled",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TLSV1_3_DOWNGRADE = MethodInfo(
        file_name="analyze_protocol",
        name="tlsv1_3_downgrade",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    HEARTBLEED_POSSIBLE = MethodInfo(
        file_name="analyze_protocol",
        name="heartbleed_possible",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    FREAK_POSSIBLE = MethodInfo(
        file_name="analyze_protocol",
        name="freak_possible",
        module="lib/ssl",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_INSECURE_PROTOCOLS = MethodInfo(
        file_name="aws",
        name="serves_content_over_insecure_protocols",
        module="lib/dast",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ELBV2_INSECURE_PROTOCOLS = MethodInfo(
        file_name="aws",
        name="elbv2_uses_insecure_ssl_protocol",
        module="lib/dast",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ELBV2_INSECURE_SSL_CIPHER = MethodInfo(
        file_name="aws",
        name="elbv2_uses_insecure_ssl_cipher",
        module="lib/dast",
        finding=FindingEnum.F016,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_JWT_SIGNED = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_jwt_signed",
        module="lib/root",
        finding=FindingEnum.F017,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/E:P/RL:X/RC:R",
        cwe_ids=["CWE-319"],
    )
    CS_VERIFY_DECODER = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_verify_decoder",
        module="lib/root",
        finding=FindingEnum.F017,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/E:P/RL:X/RC:R",
        cwe_ids=["CWE-319"],
    )
    CS_XPATH_INJECTION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_xpath_injection",
        module="lib/root",
        finding=FindingEnum.F021,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:X/RC:R",
        cwe_ids=["CWE-643"],
    )
    CS_XPATH_INJECTION_EVALUATE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_xpath_injection",
        module="lib/root",
        finding=FindingEnum.F021,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:X/RC:R",
        cwe_ids=["CWE-643"],
    )
    JAVA_XPATH_INJECTION_EVALUATE = MethodInfo(
        file_name="java",
        name="java_xpath_injection",
        module="lib/root",
        finding=FindingEnum.F021,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:X/RC:R",
        cwe_ids=["CWE-643"],
    )
    JS_DYNAMIC_X_PATH = MethodInfo(
        file_name="javascript",
        name="javascript_dynamic_xpath",
        module="lib/root",
        finding=FindingEnum.F021,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:X/RC:R",
        cwe_ids=["CWE-643"],
    )
    TS_DYNAMIC_X_PATH = MethodInfo(
        file_name="typescript",
        name="typescript_dynamic_xpath",
        module="lib/root",
        finding=FindingEnum.F021,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H/E:U/RL:X/RC:R",
        cwe_ids=["CWE-643"],
    )
    JAVA_PROP_UNENCRYPTED_TRANSPORT = MethodInfo(
        file_name="java",
        name="java_properties_unencrypted_transport",
        module="lib/path",
        finding=FindingEnum.F022,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_HTTP_GET_INSECURE_CHANNELS = MethodInfo(
        file_name="cloudformation",
        name="cfn_http_get_insecure_channel",
        module="lib/root",
        finding=FindingEnum.F022,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-319"],
    )
    LOCATION = MethodInfo(
        file_name="analyze_headers",
        name="location",
        module="lib/http",
        finding=FindingEnum.F023,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_ANYONE_ADMIN_PORTS = MethodInfo(
        file_name="cloudformation",
        name="cfn_allows_anyone_to_admin_ports",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    AWS_ANYONE_ADMIN_PORTS = MethodInfo(
        file_name="aws",
        name="allows_anyone_to_admin_ports",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_UNRESTRICTED_CIDRS = MethodInfo(
        file_name="aws",
        name="unrestricted_cidrs",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_UNRESTRICTED_IP_PROTOCOlS = MethodInfo(
        file_name="aws",
        name="unrestricted_ip_protocols",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SEC_GROUPS_RFC1918 = MethodInfo(
        file_name="aws",
        name="security_groups_ip_ranges_in_rfc1918",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_UNRESTRICTED_DNS_ACCESS = MethodInfo(
        file_name="aws",
        name="unrestricted_dns_access",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_UNRESTRICTED_FTP_ACCESS = MethodInfo(
        file_name="aws",
        name="unrestricted_ftp_access",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_OPEN_ALL_PORTS_TO_THE_PUBLIC = MethodInfo(
        file_name="aws",
        name="open_all_ports_to_the_public",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_DEFAULT_ALL_TRAFIC = MethodInfo(
        file_name="aws",
        name="default_seggroup_allows_all_traffic",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_INSTANCES_WITHOUT_PROFILE = MethodInfo(
        file_name="aws",
        name="instances_without_profile",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_INSECURE_PORT_RANGE = MethodInfo(
        file_name="aws",
        name="insecure_port_range_in_security_group",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ACL_ALLOW_EGRESS_TRAFFIC = MethodInfo(
        file_name="aws",
        name="network_acls_allow_egress_traffic",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ACL_ALLOW_ALL_INGRESS_TRAFFIC = MethodInfo(
        file_name="aws",
        name="network_acls_allow_all_ingress_traffic",
        module="lib/dast",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_EC2_SEC_GROUPS_RFC1918 = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_security_groups_ip_ranges_in_rfc1918",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_EC2_UNRESTRICTED_PORTS = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_ports",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_GROUPS_WITHOUT_EGRESS = MethodInfo(
        file_name="cloudformation",
        name="cfn_groups_without_egress",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_INST_WITHOUT_PROFILE = MethodInfo(
        file_name="cloudformation",
        name="cfn_instances_without_profile",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_UNRESTRICTED_CIDRS = MethodInfo(
        file_name="cloudformation",
        name="cfn_unrestricted_cidrs",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_UNRESTRICTED_IP_PROTO = MethodInfo(
        file_name="cloudformation",
        name="cfn_unrestricted_ip_protocols",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_EC2_OPEN_ALL_PORTS_PUBLIC = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_open_all_ports_to_the_public",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_EC2_UNRESTRICTED_DNS = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_dns_access",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    CFN_EC2_UNRESTRICTED_FTP = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unrestricted_ftp_access",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_ANYONE_ADMIN_PORTS = MethodInfo(
        file_name="terraform",
        name="tfm_allows_anyone_to_admin_ports",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_EC2_SEC_GROUPS_RFC1918 = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_security_groups_ip_ranges_in_rfc1918",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_EC2_UNRESTRICTED_DNS = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_unrestricted_dns_access",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_EC2_UNRESTRICTED_FTP = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_unrestricted_ftp_access",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_EC2_OPEN_ALL_PORTS_PUBLIC = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_open_all_ports_to_the_public",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_AWS_EC2_ALL_TRAFFIC = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ec2_allows_all_outbound_traffic",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_INST_WITHOUT_PROFILE = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_instances_without_profile",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_AWS_EC2_CFN_UNRESTR_IP_PROT = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ec2_cfn_unrestricted_ip_protocols",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_AWS_EC2_UNRESTRICTED_CIDRS = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ec2_unrestricted_cidrs",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    TFM_EC2_UNRESTRICTED_PORTS = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_unrestricted_ports",
        module="lib/root",
        finding=FindingEnum.F024,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:U",
        cwe_ids=["CWE-16"],
    )
    AWS_ADMIN_POLICY_ATTACHED = MethodInfo(
        file_name="aws",
        name="admin_policy_attached",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_PUBLIC_BUCKETS = MethodInfo(
        file_name="aws",
        name="public_buckets",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_VPC_ENDPOINTS_EXPOSED = MethodInfo(
        file_name="aws",
        name="vpc_endpoints_exposed",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_GROUP_WITH_INLINE_POLICY = MethodInfo(
        file_name="aws",
        name="group_with_inline_policies",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_USERS_WITH_PASSWORD_AND_ACCESS_KEYS = MethodInfo(
        file_name="aws",
        name="users_with_password_and_access_keys",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_POLICIES_ATTACHED_TO_USERS = MethodInfo(
        file_name="aws",
        name="policies_attached_to_users",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_USER_WITH_INLINE_POLICY = MethodInfo(
        file_name="aws",
        name="user_with_inline_policies",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_OPEN_PASSROLE = MethodInfo(
        file_name="aws",
        name="open_passrole",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_PERMISSIVE_POLICY = MethodInfo(
        file_name="aws",
        name="permissive_policy",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_HAS_PERMISSIVE_ROLE_POLICY = MethodInfo(
        file_name="aws",
        name="has_permissive_role_policies",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_FULL_ACCESS_SSM = MethodInfo(
        file_name="aws",
        name="full_access_to_ssm",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_FULL_ACCESS_POLICIES = MethodInfo(
        file_name="aws",
        name="group_with_inline_policies",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_NEGATIVE_STATEMENT = MethodInfo(
        file_name="aws",
        name="negative_statement",
        module="lib/dast",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_ADMIN_POLICY_ATTACHED = MethodInfo(
        file_name="cloudformation",
        name="cfn_admin_policy_attached",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    CFN_BUCKET_ALLOWS_PUBLIC = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_policy_allows_public_access",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    CFN_IAM_MISSING_SECURITY = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_user_missing_role_based_security",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    CFN_NEGATIVE_STATEMENT = MethodInfo(
        file_name="cloudformation",
        name="cfn_negative_statement",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    CFN_IAM_EXCESSIVE_ROLE_POLICY = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_excessive_role_policy",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    CFN_IAM_FULL_ACCESS_SSM = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_has_full_access_to_ssm",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    TFM_ADMIN_POLICY = MethodInfo(
        file_name="terraform",
        name="terraform_admin_policy_attached",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    TFM_ADMIN_MANAGED_POLICIES = MethodInfo(
        file_name="terraform",
        name="terraform_iam_excessive_privileges",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    TFM_BUCKET_ALLOWS_PUBLIC = MethodInfo(
        file_name="terraform",
        name="tfm_bucket_policy_allows_public_access",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    TFM_IAM_MISSING_SECURITY = MethodInfo(
        file_name="terraform",
        name="tfm_iam_user_missing_role_based_security",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    TFM_NEGATIVE_STATEMENT = MethodInfo(
        file_name="terraform",
        name="terraform_negative_statement",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    TFM_IAM_FULL_ACCESS_SSM = MethodInfo(
        file_name="terraform",
        name="tfm_iam_has_full_access_to_ssm",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    TFM_IAM_EXCESSIVE_ROLE_POLICY = MethodInfo(
        file_name="terraform",
        name="tfm_iam_excessive_role_policy",
        module="lib/root",
        finding=FindingEnum.F031,
        developer=DeveloperEnum.FLOR_CALDERON,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-250"],
    )
    KT_WEAK_RANDOM = MethodInfo(
        file_name="kotlin",
        name="kotlin_weak_random",
        module="lib/root",
        finding=FindingEnum.F034,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-330"],
    )
    JAVA_WEAK_RANDOM_COOKIE = MethodInfo(
        file_name="java",
        name="java_weak_random",
        module="lib/root",
        finding=FindingEnum.F034,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-521"],
    )
    JS_WEAK_RANDOM = MethodInfo(
        file_name="javascript",
        name="javascript_weak_random",
        module="lib/root",
        finding=FindingEnum.F034,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-330"],
    )
    TS_WEAK_RANDOM = MethodInfo(
        file_name="typescript",
        name="typescript_weak_random",
        module="lib/root",
        finding=FindingEnum.F034,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-330"],
    )
    CS_WEAK_CREDENTIAL = MethodInfo(
        file_name="c_sharp",
        name="csharp_weak_credential_policy",
        module="lib/root",
        finding=FindingEnum.F035,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:U/RC:C",
        cwe_ids=["CWE-521"],
    )
    CS_NO_PASSWORD = MethodInfo(
        file_name="c_sharp",
        name="csharp_no_password",
        module="lib/root",
        finding=FindingEnum.F035,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:U/RC:C",
        cwe_ids=["CWE-521"],
    )
    VIEW_STATE = MethodInfo(
        file_name="analyze_content",
        name="view_state",
        module="lib/http",
        finding=FindingEnum.F036,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    DOTNETCONFIG_NOT_SUPPRESS_VULN_HEADER = MethodInfo(
        file_name="dotnetconfig",
        name="dotnetconfig_not_suppress_vuln_header",
        module="lib/path",
        finding=FindingEnum.F037,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_INSEC_COOKIES = MethodInfo(
        file_name="c_sharp",
        name="csharp_insecurely_generated_cookies",
        module="lib/root",
        finding=FindingEnum.F042,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O",
        cwe_ids=["CWE-614"],
    )
    JS_INSEC_COOKIES = MethodInfo(
        file_name="javascript",
        name="js_insecurely_generated_cookies",
        module="lib/root",
        finding=FindingEnum.F042,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O",
        cwe_ids=["CWE-614"],
    )
    TS_INSEC_COOKIES = MethodInfo(
        file_name="typescript",
        name="typescript_insecurely_generated_cookies",
        module="lib/root",
        finding=FindingEnum.F042,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O",
        cwe_ids=["CWE-614"],
    )
    CONTENT_SECURITY_POLICY = MethodInfo(
        file_name="analyze_headers",
        name="content_security_policy",
        module="lib/http",
        finding=FindingEnum.F043,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    UPGRADE_INSEC_REQ = MethodInfo(
        file_name="analyze_headers",
        name="upgrade_insecure_requests",
        module="lib/http",
        finding=FindingEnum.F043,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_HTTP_METHODS_ENABLED = MethodInfo(
        file_name="cloudformation",
        name="cnf_http_methods_enabled",
        module="lib/root",
        finding=FindingEnum.F044,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-650"],
    )
    TFM_HTTP_METHODS_ENABLED = MethodInfo(
        file_name="terraform",
        name="tfm_http_methods_enabled",
        module="lib/root",
        finding=FindingEnum.F044,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-650"],
    )
    TFM_API_ALL_HTTP_METHODS_ENABLED = MethodInfo(
        file_name="terraform",
        name="tfm_api_all_http_methods_enabled",
        module="lib/root",
        finding=FindingEnum.F044,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-650"],
    )
    XML_HEADER_ALLOW_ALL_METHODS = MethodInfo(
        file_name="conf_files",
        name="xml_header_allow_all_methods",
        module="lib/path",
        finding=FindingEnum.F044,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
    )
    XML_HEADER_ALLOW_DANGER_METHODS = MethodInfo(
        file_name="conf_files",
        name="xml_header_allow_danger_methods",
        module="lib/path",
        finding=FindingEnum.F044,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
    )
    NO_OBFUSCATION = MethodInfo(
        file_name="analyze_bytecodes",
        name="no_obfuscation",
        module="lib/apk",
        finding=FindingEnum.F046,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    NO_ROOT_CHECK = MethodInfo(
        file_name="analyze_bytecodes",
        name="no_root_check",
        module="lib/apk",
        finding=FindingEnum.F048,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_PROP_MISSING_SSL = MethodInfo(
        file_name="java",
        name="java_properties_missing_ssl",
        module="lib/path",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_PROP_WEAK_CIPHER = MethodInfo(
        file_name="java",
        name="java_properties_weak_cipher_suite",
        module="lib/path",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_INSECURE_HASH = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_hash",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-310"],
    )
    CS_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CS_INSECURE_CIPHER = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-310"],
    )
    CS_MANAGED_SECURE_MODE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_managed_secure_mode",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-310"],
    )
    CS_RSA_SECURE_MODE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_rsa_secure_mode",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-310"],
    )
    CS_INSECURE_KEYS = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_keys",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-310"],
    )
    CS_DISABLED_STRONG_CRYPTO = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_disabled_strong_crypto",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-310"],
    )
    CS_OBSOLETE_KEY_DERIVATION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_obsolete_key_derivation",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-310"],
    )
    SWIFT_INSECURE_CIPHER = MethodInfo(
        file_name="swift",
        name="swift_insecure_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
    )
    SWIFT_INSECURE_CRYPTOR = MethodInfo(
        file_name="swift",
        name="swift_insecure_cryptor",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
    )
    SWIFT_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="swift",
        name="swift_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    GO_INSECURE_HASH = MethodInfo(
        file_name="go",
        name="go_insecure_hash",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    GO_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="go",
        name="go_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    GO_INSECURE_CIPHER = MethodInfo(
        file_name="go",
        name="go_insecure_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_INSECURE_CIPHER = MethodInfo(
        file_name="java",
        name="java_insecure_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_CIPHER_JMQI = MethodInfo(
        file_name="java",
        name="java_insecure_cipher_jmqi",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_CIPHER_SSL = MethodInfo(
        file_name="java",
        name="java_insecure_cipher_ssl",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_CONNECTION = MethodInfo(
        file_name="java",
        name="java_insecure_connection",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FLOR_CALDERON,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_HASH = MethodInfo(
        file_name="java",
        name="java_insecure_hash",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_KEY = MethodInfo(
        file_name="java",
        name="java_insecure_key",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_KEY_EC = MethodInfo(
        file_name="java",
        name="java_insecure_key_ec",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_KEY_RSA = MethodInfo(
        file_name="java",
        name="java_insecure_key_rsa",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_KEY_SECRET = MethodInfo(
        file_name="java",
        name="java_insecure_key_secret",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSECURE_PASS = MethodInfo(
        file_name="java",
        name="java_insecure_pass",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JAVA_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="java",
        name="java_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSECURE_ENCRYPT = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_encrypt",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_INSECURE_ENCRYPT = MethodInfo(
        file_name="typescript",
        name="typescript_insecure_encrypt",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSECURE_CREATE_CIPHER = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_create_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSECURE_ECDH_KEY = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_ecdh_key",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_INSECURE_ECDH_KEY = MethodInfo(
        file_name="typescript",
        name="ts_insecure_ecdh_key",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSECURE_EC_KEYPAIR = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_ec_keypair",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_INSECURE_EC_KEYPAIR = MethodInfo(
        file_name="typescript",
        name="typescript_insecure_ec_keypair",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSECURE_RSA_KEYPAIR = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_rsa_keypair",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_INSECURE_RSA_KEYPAIR = MethodInfo(
        file_name="typescript",
        name="ts_insecure_rsa_keypair",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSECURE_HASH = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_hash",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_INSECURE_HASH = MethodInfo(
        file_name="typescript",
        name="typescript_insecure_hash",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_INSECURE_CREATE_CIPHER = MethodInfo(
        file_name="typescript",
        name="ts_insecure_create_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_CIPHER = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_CIPHER_HTTP = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_CIPHER_SSL = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_HASH = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_hash",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_KEY = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_key",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_INIT_VECTOR = MethodInfo(
        file_name="kotlin",
        name="kt_insecure_init_vector",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_HOST_VERIFICATION = MethodInfo(
        file_name="kotlin",
        name="kt_insecure_host_verification",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_CERTIFICATE_VALIDATION = MethodInfo(
        file_name="kotlin",
        name="kt_insecure_certificate_validation",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_KEY_GEN = MethodInfo(
        file_name="kotlin",
        name="kt_insecure_key_gen",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_KEY_PAIR_GEN = MethodInfo(
        file_name="kotlin",
        name="kt_insecure_key_pair_gen",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_PARAMETER_SPEC = MethodInfo(
        file_name="kotlin",
        name="kt_insecure_parameter_spec",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_ENCRIPTION_KEY = MethodInfo(
        file_name="kotlin",
        name="kt_insecure_encription_key",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSECURE_KEY_EC = MethodInfo(
        file_name="kotlin",
        name="kotlin_insecure_key",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    KT_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="kotlin",
        name="kt_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    WEAK_CIPHERS_ALLOWED = MethodInfo(
        file_name="analyze_protocol",
        name="weak_ciphers_allowed",
        module="lib/ssl",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSECURE_HASH_LIBRARY = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_hash_library",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    PYTHON_INSEC_HASH_LIBRARY = MethodInfo(
        file_name="python",
        name="python_insec_hash_library",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    PYTHON_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="python",
        name="python_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_JWT_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="javascript",
        name="javascript_jwt_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_JWT_INSEC_SIGN_ALGORITHM = MethodInfo(
        file_name="typescript",
        name="typescript_jwt_insec_sign_algorithm",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_JWT_INSEC_SIGN_ALGO_ASYNC = MethodInfo(
        file_name="javascript",
        name="javascript_jwt_insec_sign_algo_async",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_JWT_INSEC_SIGN_ALGO_ASYNC = MethodInfo(
        file_name="typescript",
        name="typescript_jwt_insec_sign_algo_async",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    JS_INSEC_MSG_AUTH_MECHANISM = MethodInfo(
        file_name="javascript",
        name="javascript_insec_msg_auth_mechanism",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    TS_INSEC_MSG_AUTH_MECHANISM = MethodInfo(
        file_name="typescript",
        name="typescript_insec_msg_auth_mechanism",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    PYTHON_UNSAFE_CIPHER = MethodInfo(
        file_name="python",
        name="python_unsafe_cipher",
        module="lib/root",
        finding=FindingEnum.F052,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C",
        cwe_ids=["CWE-310"],
    )
    APK_BACKUPS_ENABLED = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_backups_enabled",
        module="lib/apk",
        finding=FindingEnum.F055,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    PATH_APK_BACKUPS_ENABLED = MethodInfo(
        file_name="android",
        name="apk_backups_enabled",
        module="lib/path",
        finding=FindingEnum.F055,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JSON_ANON_CONNECTION_CONFIG = MethodInfo(
        file_name="conf_files",
        name="json_anon_connection_config",
        module="lib/root",
        finding=FindingEnum.F056,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N/E:X/RL:O/RC:X",
        cwe_ids=["CWE-284"],
    )
    APK_DEBUGGING_ENABLED = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_debugging_enabled",
        module="lib/apk",
        finding=FindingEnum.F058,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    PATH_APK_DEBUGGING_ENABLED = MethodInfo(
        file_name="android",
        name="apk_debugging_enabled",
        module="lib/path",
        finding=FindingEnum.F058,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_SENSITIVE_INFO_IN_LOGS = MethodInfo(
        file_name="java",
        name="java_sensitive_log_info",
        module="lib/root",
        finding=FindingEnum.F059,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N/E:P/RC:R",
        cwe_ids=["CWE-209"],
    )
    DOTNETCONFIG_HAS_SSL_DISABLED = MethodInfo(
        file_name="dotnetconfig",
        name="dotnetconfig_has_ssl_disabled",
        module="lib/path",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    XML_ALLOWS_ALL_DOMAINS = MethodInfo(
        file_name="conf_files",
        name="xml_allows_all_domains",
        module="lib/path",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    JSON_DISABLE_HOST_CHECK = MethodInfo(
        file_name="conf_files",
        name="json_disable_host_check",
        module="lib/root",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    CS_INSECURE_CERTIFICATE_VALIDATION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_certificate_validation",
        module="lib/root",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-396"],
    )
    NOT_VERIFIES_SSL_HOSTNAME = MethodInfo(
        file_name="analyze_bytecodes",
        name="not_verifies_ssl_hostname",
        module="lib/apk",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    JSON_ALLOWED_HOSTS = MethodInfo(
        file_name="conf_files",
        name="json_allowed_hosts",
        module="lib/root",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    TS_UNSAFE_ORIGIN = MethodInfo(
        file_name="typescript",
        name="typescript_unsafe_origin",
        module="lib/root",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    JS_UNSAFE_ORIGIN = MethodInfo(
        file_name="javascript",
        name="javascript_unsafe_origin",
        module="lib/root",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    PYTHON_UNSAFE_SSL_HOSTNAME = MethodInfo(
        file_name="python",
        name="python_unsafe_ssl_hostname",
        module="lib/root",
        finding=FindingEnum.F060,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-396"],
    )
    TS_ZIP_SLIP = MethodInfo(
        file_name="typescript",
        name="ts_zip_slip",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:X/RL:X/RC:X",
        cwe_ids=["CWE-22"],
    )
    JS_ZIP_SLIP = MethodInfo(
        file_name="javascript",
        name="js_zip_slip",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:X/RL:X/RC:X",
        cwe_ids=["CWE-22"],
    )
    PYTHON_IO_PATH_TRAVERSAL = MethodInfo(
        file_name="python",
        name="python_io_path_traversal",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:X/RL:X/RC:X",
        cwe_ids=["CWE-22"],
    )
    CS_OPEN_REDIRECT = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_open_redirect",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RC:U",
        cwe_ids=["CWE-22"],
    )
    CS_UNSAFE_PATH_TRAVERSAL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_unsafe_path_traversal",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RC:U",
        cwe_ids=["CWE-22"],
    )
    JAVA_ZIP_SLIP_PATH_INJECTION = MethodInfo(
        file_name="java",
        name="java_zip_slip_injection",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.FLOR_CALDERON,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RC:U",
        cwe_ids=["CWE-22"],
    )
    JAVA_UNSAFE_PATH_TRAVERSAL = MethodInfo(
        file_name="java",
        name="java_unsafe_path_traversal",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RC:U",
        cwe_ids=["CWE-22"],
    )
    JS_PATH_TRAVERSAL = MethodInfo(
        file_name="javascript",
        name="js_insecure_path_traversal",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.FLOR_CALDERON,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TS_PATH_TRAVERSAL = MethodInfo(
        file_name="typescript",
        name="ts_insecure_path_traversal",
        module="lib/root",
        finding=FindingEnum.F063,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:X/RL:X/RC:X",
        cwe_ids=["CWE-22"],
    )
    DATE = MethodInfo(
        file_name="analyze_headers",
        name="date",
        module="lib/http",
        finding=FindingEnum.F064,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    HTML_HAS_AUTOCOMPLETE = MethodInfo(
        file_name="html",
        name="html_has_autocomplete",
        module="lib/path",
        finding=FindingEnum.F065,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_HAS_CONSOLE_FUNCTIONS = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_has_console_functions",
        module="lib/root",
        finding=FindingEnum.F066,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O",
        cwe_ids=["CWE-200"],
    )
    JS_USES_CONSOLE_LOG = MethodInfo(
        file_name="javascript",
        name="js_uses_console_log",
        module="lib/root",
        finding=FindingEnum.F066,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-200"],
    )
    TS_USES_CONSOLE_LOG = MethodInfo(
        file_name="typescript",
        name="ts_uses_console_log",
        module="lib/root",
        finding=FindingEnum.F066,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-200"],
    )
    AWS_INSECURE_SECURITY_POLICY = MethodInfo(
        file_name="aws",
        name="uses_insecure_security_policy",
        module="lib/dast",
        finding=FindingEnum.F070,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EKS_INSECURE_INBOUND_TRAFFIC = MethodInfo(
        file_name="aws",
        name="eks_allows_insecure_inbound_traffic",
        module="lib/dast",
        finding=FindingEnum.F070,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_ELB2_INSECURE_SEC_POLICY = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_uses_insecure_security_policy",
        module="lib/root",
        finding=FindingEnum.F070,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-266"],
    )
    TFM_ELB2_INSECURE_SEC_POLICY = MethodInfo(
        file_name="terraform",
        name="tfm_elb2_uses_insecure_security_policy",
        module="lib/root",
        finding=FindingEnum.F070,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-266"],
    )
    REFERRER_POLICY = MethodInfo(
        file_name="analyze_headers",
        name="referrer_policy",
        module="lib/http",
        finding=FindingEnum.F071,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_HAS_PUBLIC_INSTANCES = MethodInfo(
        file_name="aws",
        name="has_public_instances",
        module="lib/dast",
        finding=FindingEnum.F073,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_RDS_PUB_ACCESSIBLE = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_is_publicly_accessible",
        module="lib/root",
        finding=FindingEnum.F073,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-478"],
    )
    TFM_RDS_PUB_ACCESSIBLE = MethodInfo(
        file_name="terraform",
        name="tfm_db_instance_publicly_accessible",
        module="lib/root",
        finding=FindingEnum.F073,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-478"],
    )
    APK_EXPORTED_CP = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_exported_cp",
        module="lib/apk",
        finding=FindingEnum.F075,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    PATH_APK_EXPORTED_CP = MethodInfo(
        file_name="android",
        name="apk_exported_cp",
        module="lib/path",
        finding=FindingEnum.F075,
        developer=DeveloperEnum.BRIAM_AGUDELO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    NON_UPGRADEABLE_DEPS = MethodInfo(
        file_name="generic",
        name="non_upgradeable_deps",
        module="lib/path",
        finding=FindingEnum.F079,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_HAS_MFA_DISABLED = MethodInfo(
        file_name="aws",
        name="iam_has_mfa_disabled",
        module="lib/dast",
        finding=FindingEnum.F081,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_COGNITO_HAS_MFA_DISABLED = MethodInfo(
        file_name="aws",
        name="cognito_has_mfa_disabled",
        module="lib/dast",
        finding=FindingEnum.F081,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_MFA_DISABLED_FOR_USERS_WITH_CONSOLE_PASSWD = MethodInfo(
        file_name="aws",
        name="mfa_disabled_for_users_with_console_password",
        module="lib/dast",
        finding=FindingEnum.F081,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_ROOT_HAS_MFA_DISABLED = MethodInfo(
        file_name="aws",
        name="root_without_mfa",
        module="lib/dast",
        finding=FindingEnum.F081,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    USES_INSECURE_DELETE = MethodInfo(
        file_name="analyze_bytecodes",
        name="uses_insecure_delete",
        module="lib/apk",
        finding=FindingEnum.F082,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    SOCKET_GET_INSECURE = MethodInfo(
        file_name="analyze_bytecodes",
        name="socket_uses_get_insecure",
        module="lib/apk",
        finding=FindingEnum.F082,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    JS_XML_PARSER = MethodInfo(
        file_name="javascript",
        name="js_xml_parser",
        module="lib/root",
        finding=FindingEnum.F083,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-611"],
    )
    TS_XML_PARSER = MethodInfo(
        file_name="typescript",
        name="ts_xml_parser",
        module="lib/root",
        finding=FindingEnum.F083,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-611"],
    )
    PYTHON_XML_PARSER = MethodInfo(
        file_name="python",
        name="python_xml_parser",
        module="lib/root",
        finding=FindingEnum.F083,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-611"],
    )
    JAVA_XML_PARSER = MethodInfo(
        file_name="java",
        name="java_xml_parser",
        module="lib/root",
        finding=FindingEnum.F083,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:P/RL:O/RC:X",
        cwe_ids=["CWE-611"],
    )
    KT_XML_PARSER = MethodInfo(
        file_name="kotlin",
        name="kt_xml_parser",
        module="lib/root",
        finding=FindingEnum.F083,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-611"],
    )
    JS_CLIENT_STORAGE = MethodInfo(
        file_name="javascript",
        name="javascript_client_storage",
        module="lib/root",
        finding=FindingEnum.F085,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-922"],
    )
    TS_CLIENT_STORAGE = MethodInfo(
        file_name="typescript",
        name="typescript_client_storage",
        module="lib/root",
        finding=FindingEnum.F085,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-922"],
    )
    HTML_HAS_NOT_SUB_RESOURCE_INTEGRITY = MethodInfo(
        file_name="html",
        name="html_has_not_sub_resource_integrity",
        module="lib/path",
        finding=FindingEnum.F086,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    SUB_RESOURCE_INTEGRITY = MethodInfo(
        file_name="analyze_content",
        name="sub_resource_integrity",
        module="lib/http",
        finding=FindingEnum.F086,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_TRUST_BOUNDARY_VIOLATION = MethodInfo(
        file_name="java",
        name="java_trust_boundary_violation",
        module="lib/root",
        finding=FindingEnum.F089,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-501"],
    )
    JS_JSON_PARSE_UNVALIDATED_DATA = MethodInfo(
        file_name="javascript",
        name="javascript_json_parse_unvalidated_data",
        module="lib/root",
        finding=FindingEnum.F089,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-501"],
    )
    TS_JSON_PARSE_UNVALIDATED_DATA = MethodInfo(
        file_name="typescript",
        name="typescript_json_parse_unvalidated_data",
        module="lib/root",
        finding=FindingEnum.F089,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-501"],
    )
    CS_INSECURE_LOGGING = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_logging",
        module="lib/root",
        finding=FindingEnum.F091,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U",
        cwe_ids=["CWE-117"],
    )
    JAVA_INSECURE_LOGGING = MethodInfo(
        file_name="java",
        name="java_insecure_logging",
        module="lib/root",
        finding=FindingEnum.F091,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U",
        cwe_ids=["CWE-117"],
    )
    DART_INSECURE_LOGGING = MethodInfo(
        file_name="dart",
        name="dart_insecure_logging",
        module="lib/root",
        finding=FindingEnum.F091,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U",
        cwe_ids=["CWE-117"],
    )
    JS_INSECURE_LOGGING = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_logging",
        module="lib/root",
        finding=FindingEnum.F091,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U",
        cwe_ids=["CWE-117"],
    )
    TS_INSECURE_LOGGING = MethodInfo(
        file_name="typescript",
        name="typescript_insecure_logging",
        module="lib/root",
        finding=FindingEnum.F091,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U",
        cwe_ids=["CWE-117"],
    )
    CBC_ENABLED = MethodInfo(
        file_name="analyze_protocol",
        name="cbc_enabled",
        module="lib/ssl",
        finding=FindingEnum.F094,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_INSECURE_DESERIAL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insecure_deserialization",
        module="lib/root",
        finding=FindingEnum.F096,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:L/E:P",
        cwe_ids=["CWE-502"],
    )
    CS_XML_SERIAL = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_check_xml_serializer",
        module="lib/root",
        finding=FindingEnum.F096,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:L/E:P",
        cwe_ids=["CWE-502"],
    )
    CS_JS_DESERIALIZATION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_js_deserialization",
        module="lib/root",
        finding=FindingEnum.F096,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:L/E:P",
        cwe_ids=["CWE-502"],
    )
    CS_TYPE_NAME_HANDLING = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_type_name_handling",
        module="lib/root",
        finding=FindingEnum.F096,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:L/E:P",
        cwe_ids=["CWE-502"],
    )
    PYTHON_DESERIALIZATION_INJECTION = MethodInfo(
        file_name="python",
        name="python_deserialization_injection",
        module="lib/root",
        finding=FindingEnum.F096,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:C/C:N/I:L/A:L/E:U",
        cwe_ids=["CWE-502"],
    )
    HTML_HAS_REVERSE_TABNABBING = MethodInfo(
        file_name="html",
        name="html_has_reverse_tabnabbing",
        module="lib/path",
        finding=FindingEnum.F097,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JS_HAS_REVERSE_TABNABBING = MethodInfo(
        file_name="javascript",
        name="javascript_has_reverse_tabnabbing",
        module="lib/root",
        finding=FindingEnum.F097,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-502"],
    )
    TS_HAS_REVERSE_TABNABBING = MethodInfo(
        file_name="typescript",
        name="typescript_has_reverse_tabnabbing",
        module="lib/root",
        finding=FindingEnum.F097,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-502"],
    )
    CS_PATH_INJECTION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_path_injection",
        module="lib/root",
        finding=FindingEnum.F098,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:P",
        cwe_ids=["CWE-22"],
    )
    AWS_BUCKET_POLICY_ENCRYPTION_DISABLE = MethodInfo(
        file_name="aws",
        name="bucket_policy_has_server_side_encryption_disable",
        module="lib/dast",
        finding=FindingEnum.F099,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_POLICY_SERVER_ENCRYP_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_policy_has_server_side_encryption_disabled",
        module="lib/root",
        finding=FindingEnum.F099,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-311"],
    )
    TFM_POLICY_SERVER_ENCRYP_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_bucket_policy_has_server_side_encryption_disabled",
        module="lib/root",
        finding=FindingEnum.F099,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-311"],
    )
    CS_INSEC_CREATE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_insec_create",
        module="lib/root",
        finding=FindingEnum.F100,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:H/A:L/E:P/RL:X/RC:X",
        cwe_ids=["CWE-918"],
    )
    AWS_S3_BUCKETS_HAS_OBJECT_LOCK_DISABLED = MethodInfo(
        file_name="aws",
        name="bucket_has_object_lock_disabled",
        module="lib/dast",
        finding=FindingEnum.F101,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    APK_UNSIGNED = MethodInfo(
        file_name="analyze_bytecodes",
        name="apk_unsigned",
        module="lib/apk",
        finding=FindingEnum.F103,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_LDAP_INJECTION = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_ldap_injection",
        module="lib/root",
        finding=FindingEnum.F107,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N/E:P/RL:O/RC:X",
        cwe_ids=["CWE-90"],
    )
    KT_ANONYMOUS_LDAP = MethodInfo(
        file_name="kotlin",
        name="kt_anonymous_ldap",
        module="lib/root",
        finding=FindingEnum.F107,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N/E:P/RL:O/RC:X",
        cwe_ids=["CWE-90"],
    )
    JAVA_LDAP_INJECTION = MethodInfo(
        file_name="java",
        name="java_ldap_injection",
        module="lib/root",
        finding=FindingEnum.F107,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N/E:P/RL:O/RC:U",
        cwe_ids=["CWE-90"],
    )
    PYTHON_LDAP_INJECTION = MethodInfo(
        file_name="python",
        name="python_ldap_injection",
        module="lib/root",
        finding=FindingEnum.F107,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N/E:P/RL:O/RC:X",
        cwe_ids=["CWE-90"],
    )
    AWS_NOT_INSIDE_A_DB_SUBNET_GROUP = MethodInfo(
        file_name="aws",
        name="is_not_inside_a_db_subnet_group",
        module="lib/dast",
        finding=FindingEnum.F109,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_RDS_UNRESTRICTED_DB_SECURITY_GROUPS = MethodInfo(
        file_name="aws",
        name="rds_unrestricted_db_security_groups",
        module="lib/dast",
        finding=FindingEnum.F109,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_RDS_NOT_INSIDE_DB_SUBNET = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_is_not_inside_a_db_subnet_group",
        module="lib/root",
        finding=FindingEnum.F109,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-681"],
    )
    TFM_RDS_INSIDE_SUBNET = MethodInfo(
        file_name="terraform",
        name="tfm_rds_instance_inside_subnet",
        module="lib/root",
        finding=FindingEnum.F109,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-681"],
    )
    JAVA_SQL_INJECTION = MethodInfo(
        file_name="java",
        name="java_sql_injection",
        module="lib/root",
        finding=FindingEnum.F112,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N/E:P/RC:R",
        cwe_ids=["CWE-89"],
    )
    JS_SQL_API_INJECTION = MethodInfo(
        file_name="javascript",
        name="javascript_sql_api_injection",
        module="lib/root",
        finding=FindingEnum.F112,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:X/RC:R",
        cwe_ids=["CWE-89"],
    )
    TS_SQL_API_INJECTION = MethodInfo(
        file_name="typescript",
        name="typescript_sql_api_injection",
        module="lib/root",
        finding=FindingEnum.F112,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:X/RC:R",
        cwe_ids=["CWE-89"],
    )
    UNVERIFIABLE_FILES = MethodInfo(
        file_name="generic",
        name="unverifiable_files",
        module="lib/path",
        finding=FindingEnum.F117,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    PIP_INCOMPLETE_DEPENDENCIES_LIST = MethodInfo(
        file_name="python",
        name="pip_incomplete_dependencies_list",
        module="lib/sca",
        finding=FindingEnum.F120,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    GO_INSECURE_QUERY_FLOAT = MethodInfo(
        file_name="go",
        name="go_insecure_query_float",
        module="lib/root",
        finding=FindingEnum.F127,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:L/E:U/RL:X/RC:X",
        cwe_ids=["CWE-843"],
    )
    SET_COOKIE_HTTPONLY = MethodInfo(
        file_name="analyze_headers",
        name="set_cookie_httponly",
        module="lib/http",
        finding=FindingEnum.F128,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_HTTP_ONLY_COOKIE = MethodInfo(
        file_name="java",
        name="java_http_only_cookie",
        module="lib/root",
        finding=FindingEnum.F128,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-1004"],
    )
    KOTLIN_HTTP_ONLY_COOKIE = MethodInfo(
        file_name="kotlin",
        name="kotlin_http_only_cookie",
        module="lib/root",
        finding=FindingEnum.F128,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-1004"],
    )
    PYTHON_HTTP_ONLY_COOKIE = MethodInfo(
        file_name="python",
        name="python_http_only_cookie",
        module="lib/root",
        finding=FindingEnum.F128,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-1004"],
    )
    JS_INSECURE_COOKIE = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_cookie",
        module="lib/root",
        finding=FindingEnum.F128,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-1004"],
    )
    TS_INSECURE_COOKIE = MethodInfo(
        file_name="typescript",
        name="typescript_insecure_cookie",
        module="lib/root",
        finding=FindingEnum.F128,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-1004"],
    )
    SET_COOKIE_SAMESITE = MethodInfo(
        file_name="analyze_headers",
        name="set_cookie_samesite",
        module="lib/http",
        finding=FindingEnum.F129,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    SET_COOKIE_SECURE = MethodInfo(
        file_name="analyze_headers",
        name="set_cookie_secure",
        module="lib/http",
        finding=FindingEnum.F130,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_SECURE_COOKIE = MethodInfo(
        file_name="java",
        name="java_secure_cookie",
        module="lib/root",
        finding=FindingEnum.F130,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-614"],
    )
    KOTLIN_SECURE_COOKIE = MethodInfo(
        file_name="kotlin",
        name="kotlin_secure_cookie",
        module="lib/root",
        finding=FindingEnum.F130,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-614"],
    )
    PYTHON_SECURE_COOKIE = MethodInfo(
        file_name="python",
        name="python_secure_cookie",
        module="lib/root",
        finding=FindingEnum.F130,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-614"],
    )
    STRICT_TRANSPORT_SECURITY = MethodInfo(
        file_name="analyze_headers",
        name="strict_transport_security",
        module="lib/http",
        finding=FindingEnum.F131,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    X_CONTENT_TYPE_OPTIONS = MethodInfo(
        file_name="analyze_headers",
        name="x_content_type_options",
        module="lib/http",
        finding=FindingEnum.F132,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    PFS_DISABLED = MethodInfo(
        file_name="analyze_protocol",
        name="pfs_disabled",
        module="lib/ssl",
        finding=FindingEnum.F133,
        developer=DeveloperEnum.ALEJANDRO_SALGADO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_WILDCARD_IN_ALLOWED_ORIGINS = MethodInfo(
        file_name="cloudformation",
        name="cfn_wildcard_in_allowed_origins",
        module="lib/root",
        finding=FindingEnum.F134,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-614"],
    )
    YML_SERVERLESS_CORS = MethodInfo(
        file_name="cloudformation",
        name="json_ssl_port_missing",
        module="lib/root",
        finding=FindingEnum.F134,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
    )
    CS_INSECURE_CORS = MethodInfo(
        file_name="c_sharp",
        name="csharp_insecure_cors",
        module="lib/root",
        finding=FindingEnum.F134,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_INSECURE_CORS_ORIGIN = MethodInfo(
        file_name="c_sharp",
        name="csharp_insecure_cors_origin",
        module="lib/root",
        finding=FindingEnum.F134,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:U/RC:C",
        cwe_ids=["CWE-16"],
    )
    JAVA_INSECURE_CORS_ORIGIN = MethodInfo(
        file_name="java",
        name="java_insecure_cors_origin",
        module="lib/root",
        finding=FindingEnum.F134,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:U/RC:C",
        cwe_ids=["CWE-16"],
    )
    JS_UNSAFE_HTTP_XSS_PROTECTION = MethodInfo(
        file_name="javascript",
        name="javascript_unsafe_http_xss_protection",
        module="lib/root",
        finding=FindingEnum.F135,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-644"],
    )
    TS_UNSAFE_HTTP_XSS_PROTECTION = MethodInfo(
        file_name="typescript",
        name="typescript_unsafe_http_xss_protection",
        module="lib/root",
        finding=FindingEnum.F135,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-644"],
    )
    XML_HAS_X_XSS_PROTECTION_HEADER = MethodInfo(
        file_name="conf_files",
        name="xml_has_x_xss_protection_header",
        module="lib/path",
        finding=FindingEnum.F135,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    JS_USES_EVAL = MethodInfo(
        file_name="javascript",
        name="js_uses_eval",
        module="lib/root",
        finding=FindingEnum.F143,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:X/RC:X",
        cwe_ids=["CWE-676"],
    )
    TS_USES_EVAL = MethodInfo(
        file_name="typescript",
        name="ts_uses_eval",
        module="lib/root",
        finding=FindingEnum.F143,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:X/RC:X",
        cwe_ids=["CWE-676"],
    )
    CS_INSECURE_CHANNEL = MethodInfo(
        file_name="c_sharp",
        name="cs_insecure_channel",
        module="lib/root",
        finding=FindingEnum.F148,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-319"],
    )
    XML_NETWORK_SSL_DISABLED = MethodInfo(
        file_name="conf_files",
        name="xml_network_ssl_disabled",
        module="lib/path",
        finding=FindingEnum.F149,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    JS_UNSAFE_HTTP_X_FRAME_OPTIONS = MethodInfo(
        file_name="javascript",
        name="javascript_unsafe_http_xframe_options",
        module="lib/root",
        finding=FindingEnum.F152,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-693"],
    )
    TS_UNSAFE_HTTP_X_FRAME_OPTIONS = MethodInfo(
        file_name="typescript",
        name="typescript_unsafe_http_xframe_options",
        module="lib/root",
        finding=FindingEnum.F152,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-693"],
    )
    XML_X_FRAME_OPTIONS = MethodInfo(
        file_name="conf_files",
        name="xml_x_frame_options",
        module="lib/path",
        finding=FindingEnum.F152,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-693"],
    )
    C_SHARP_ACCEPTS_ANY_MIMETYPE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_accepts_any_mime_type_chain",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    JAVA_ACCEPTS_ANY_MIMETYPE_CHAIN = MethodInfo(
        file_name="java",
        name="java_accepts_any_mime_type_chain",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    JAVA_HTTP_REQ_ACCEPTS_ANY_MIMETYPE = MethodInfo(
        file_name="java",
        name="java_http_accepts_any_mime_type",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    JAVASCRIPT_ACCEPTS_ANY_MIME_METHOD = MethodInfo(
        file_name="javascript",
        name="javascript_accepts_any_mime_method",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    PYTHON_ACCEPTS_ANY_MIME = MethodInfo(
        file_name="python",
        name="python_accepts_any_mime",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    GO_ACCEPTS_ANY_MIME_TYPE = MethodInfo(
        file_name="go",
        name="go_accepts_any_mime_type",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    KOTLIN_ACCEPTS_ANY_MIME_TYPE = MethodInfo(
        file_name="kotlin",
        name="kotlin_accepts_any_mime_type",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    TYPESCRIPT_ACCEPTS_ANY_MIME_METHOD = MethodInfo(
        file_name="typescript",
        name="typescript_accepts_any_mime_method",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    JAVASCRIPT_ACCEPTS_ANY_MIME_DEFAULT = MethodInfo(
        file_name="javascript",
        name="javascript_accepts_any_mime_default",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    TYPESCRIPT_ACCEPTS_ANY_MIME_DEFAULT = MethodInfo(
        file_name="typescript",
        name="typescript_accepts_any_mime_default",
        module="lib/root",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    XML_ACCEPT_HEADER = MethodInfo(
        file_name="conf_files",
        name="xml_accept_header",
        module="lib/path",
        finding=FindingEnum.F153,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    TFM_AZURE_UNRESTRICTED_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_unrestricted_access_network_segments",
        module="lib/root",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-923"],
    )
    TFM_AZURE_SA_DEFAULT_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_sa_default_network_access",
        module="lib/root",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-923"],
    )
    TFM_AZURE_KV_DEFAULT_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_default_network_access",
        module="lib/root",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-923"],
    )
    TFM_AZURE_KV_DANGER_BYPASS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_danger_bypass",
        module="lib/root",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-923"],
    )
    TFM_AWS_ACL_BROAD_NETWORK_ACCESS = MethodInfo(
        file_name="terraform",
        name="tfm_aws_acl_broad_network_access",
        module="lib/root",
        finding=FindingEnum.F157,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:L/PR:L/UI:N/S:C/C:H/I:L/A:L/E:U/RL:O/RC:X",
        cwe_ids=["CWE-923"],
    )
    CS_CREATE_TEMP_FILE = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_file_create_temp_file",
        module="lib/root",
        finding=FindingEnum.F160,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:L/I:L/A:N/E:P/RL:U/RC:C",
        cwe_ids=["CWE-378"],
    )
    JAVA_CREATE_TEMP_FILE = MethodInfo(
        file_name="java",
        name="java_file_create_temp_file",
        module="lib/root",
        finding=FindingEnum.F160,
        developer=DeveloperEnum.DIEGO_RESTREPO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:L/I:L/A:N/E:P/RL:U/RC:C",
        cwe_ids=["CWE-378"],
    )
    PYTHON_UNSAFE_TEMP_FILE = MethodInfo(
        file_name="python",
        name="python_unsafe_temp_file",
        module="lib/root",
        finding=FindingEnum.F160,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:L/AC:H/PR:H/UI:R/S:U/C:L/I:L/A:N/E:P/RL:U/RC:C",
        cwe_ids=["CWE-378"],
    )
    JSON_SSL_PORT_MISSING = MethodInfo(
        file_name="conf_files",
        name="json_ssl_port_missing",
        module="lib/root",
        finding=FindingEnum.F164,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-16"],
    )
    AWS_USER_WITH_MULTIPLE_ACCESS_KEYS = MethodInfo(
        file_name="aws",
        name="users_with_multiple_access_keys",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EKS_HAS_ENDPOINTS_PUBLICLY_ACCESSIBLE = MethodInfo(
        file_name="aws",
        name="eks_has_endpoints_publicly_accessible",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_HAS_ROOT_ACTIVE_SIGNING_CERTIFICATES = MethodInfo(
        file_name="aws",
        name="has_root_active_signing_certificates",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_HAS_NOT_SUPPORT_ROLE = MethodInfo(
        file_name="aws",
        name="has_not_support_role",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_ROOT_HAS_ACCESS_KEYS = MethodInfo(
        file_name="aws",
        name="root_has_access_keys",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_DYNAMODB_ENCRYPTED_WITH_AWS_MASTER_KEYS = MethodInfo(
        file_name="aws",
        name="dynamob_encrypted_with_aws_master_keys",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_RDS_HAS_PUBLIC_SNAPSHOTS = MethodInfo(
        file_name="aws",
        name="rds_has_public_snapshots",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_RDS_NOT_USES_IAM_AUTHENTICATION = MethodInfo(
        file_name="aws",
        name="rds_not_uses_iam_authentication",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ELASTICACHE_USES_DEFAULT_PORT = MethodInfo(
        file_name="aws",
        name="elasticache_uses_default_port",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ELASTICACHE_TRANSIT_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="elasticache_is_transit_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SNS_HAS_SERVER_SIDE_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="sns_is_server_side_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SNS_USES_DEFAULT_KMS_KEY = MethodInfo(
        file_name="aws",
        name="sns_uses_default_kms_key",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SNS_CAN_ANYONE_PUBLISH = MethodInfo(
        file_name="aws",
        name="sns_can_anyone_publish",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SNS_CAN_ANYONE_SUBSCRIBE = MethodInfo(
        file_name="aws",
        name="sns_can_anyone_subscribe",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ELASTICACHE_REST_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="elasticache_is_at_rest_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_REDSHIFT_HAS_PUBLIC_CLUSTERS = MethodInfo(
        file_name="aws",
        name="redshift_has_public_clusters",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SQS_HAS_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="sqs_is_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SQS_USES_DEFAULT_KMS_KEY = MethodInfo(
        file_name="aws",
        name="sqs_uses_default_kms_key",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_SQS_IS_PUBLIC = MethodInfo(
        file_name="aws",
        name="sqs_is_public",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_REDSHIFT_NOT_REQUIRES_SSL = MethodInfo(
        file_name="aws",
        name="redshift_not_requires_ssl",
        module="lib/dast",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TFM_IAM_PERMISSIONS_POLICY_NOT_RESOURCE = MethodInfo(
        file_name="terraform",
        name="tfm_iam_permissions_policy_allow_not_resource",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    TFM_IAM_PERMISSIONS_POLICY_NOT_ACTION = MethodInfo(
        file_name="terraform",
        name="tfm_iam_permissions_policy_allow_not_action",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    TFM_IAM_TRUST_POLICY_NOT_PRINCIPAL = MethodInfo(
        file_name="terraform",
        name="tfm_iam_role_is_over_privileged",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    TFM_IAM_TRUST_POLICY_NOT_ACTION = MethodInfo(
        file_name="terraform",
        name="cfn_iam_trust_policy_allow_not_action",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    TFM_IAM_POLICY_APPLY_TO_USERS = MethodInfo(
        file_name="terraform",
        name="tfm_iam_policy_apply_to_users",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    CFN_IAM_PERMISSIONS_POLICY_NOT_RESOURCE = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_permissions_policy_allow_not_resource",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    CFN_IAM_PERMISSIONS_POLICY_NOT_ACTION = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_permissions_policy_allow_not_action",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    CFN_IAM_TRUST_POLICY_NOT_PRINCIPAL = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_trust_policy_allow_not_principal",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    CFN_IAM_TRUST_POLICY_NOT_ACTION = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_trust_policy_allow_not_action",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    CFN_IAM_POLICY_APPLY_TO_USERS = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_permissions_policy_aplly_users",
        module="lib/root",
        finding=FindingEnum.F165,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-16"],
    )
    C_SHARP_PLAIN_TEXT_KEYS = MethodInfo(
        file_name="c_sharp",
        name="c_sharp_plain_text_keys",
        module="lib/root",
        finding=FindingEnum.F169,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-798"],
    )
    CONTAINER_USING_SSHPASS = MethodInfo(
        file_name="docker",
        name="container_using_sshpass",
        module="lib/path",
        finding=FindingEnum.F176,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
    )
    BASH_USING_SSHPASS = MethodInfo(
        file_name="bash",
        name="bash_using_sshpass",
        module="lib/path",
        finding=FindingEnum.F176,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
    )
    AWS_HAS_DEFAULT_SECURITY_GROUPS_IN_USE = MethodInfo(
        file_name="aws",
        name="has_default_security_groups_in_use",
        module="lib/dast",
        finding=FindingEnum.F177,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_DEFAULT_SECURITY_GROUP = MethodInfo(
        file_name="aws",
        name="use_default_security_group",
        module="lib/dast",
        finding=FindingEnum.F177,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_EC2_DEFAULT_SEC_GROUP = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_use_default_security_group",
        module="lib/root",
        finding=FindingEnum.F177,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    EC2_DEFAULT_SEC_GROUP = MethodInfo(
        file_name="terraform",
        name="ec2_use_default_security_group",
        module="lib/root",
        finding=FindingEnum.F177,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    CHECK_DNS_RECORDS = MethodInfo(
        file_name="analyze_dns",
        name="check_dns_records",
        module="lib/http",
        finding=FindingEnum.F182,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    DOTNETCONFIG_HAS_DEBUG_ENABLED = MethodInfo(
        file_name="dotnetconfig",
        name="dotnetconfig_has_debug_enabled",
        module="lib/path",
        finding=FindingEnum.F183,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JS_DEBUGGER_ENABLED = MethodInfo(
        file_name="javascript",
        name="js_debugger_enabled",
        module="lib/root",
        finding=FindingEnum.F183,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-489"],
    )
    TS_DEBUGGER_ENABLED = MethodInfo(
        file_name="typescript",
        name="ts_debugger_enabled",
        module="lib/root",
        finding=FindingEnum.F183,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-489"],
    )
    TSX_LACK_OF_VALIDATION_EVENT_LISTENER = MethodInfo(
        file_name="typescript",
        name="tsx_lack_of_validation_event_listener",
        module="lib/root",
        finding=FindingEnum.F188,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-489"],
    )
    JSX_LACK_OF_VALIDATION_EVENT_LISTENER = MethodInfo(
        file_name="javascript",
        name="tsx_lack_of_validation_event_listener",
        module="lib/root",
        finding=FindingEnum.F188,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-489"],
    )
    AWS_VPC_WITHOUT_FLOWLOG = MethodInfo(
        file_name="aws",
        name="vpcs_without_flowlog",
        module="lib/dast",
        finding=FindingEnum.F200,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_REDSHIFT_HAS_AUDIT_LOGS_DISABLED = MethodInfo(
        file_name="aws",
        name="redshift_has_audit_logging_disabled",
        module="lib/dast",
        finding=FindingEnum.F200,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_REDSHIFT_HAS_USER_ACTIVITY_LOG_DISABLED = MethodInfo(
        file_name="aws",
        name="redshift_is_user_activity_logging_disabled",
        module="lib/dast",
        finding=FindingEnum.F200,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ACL_PUBLIC_BUCKETS = MethodInfo(
        file_name="aws",
        name="acl_public_buckets",
        module="lib/dast",
        finding=FindingEnum.F203,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_IS_TRAIL_BUCKET_PUBLIC = MethodInfo(
        file_name="aws",
        name="is_trail_bucket_public",
        module="lib/dast",
        finding=FindingEnum.F203,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_S3_BUCKETS_ALLOW_UNAUTHORIZED_PUBLIC_ACCESS = MethodInfo(
        file_name="aws",
        name="s3_buckets_allow_unauthorized_public_access",
        module="lib/dast",
        finding=FindingEnum.F203,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_PUBLIC_BUCKETS = MethodInfo(
        file_name="cloudformation",
        name="cfn_public_buckets",
        module="lib/root",
        finding=FindingEnum.F203,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-284"],
    )
    TFM_PUBLIC_BUCKETS = MethodInfo(
        file_name="terraform",
        name="tfm_public_buckets",
        module="lib/root",
        finding=FindingEnum.F203,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-284"],
    )
    HAS_FRIDA = MethodInfo(
        file_name="analyze_bytecodes",
        name="has_frida",
        module="lib/apk",
        finding=FindingEnum.F206,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    NO_CERTS_PINNING = MethodInfo(
        file_name="analyze_bytecodes",
        name="no_certs_pinning",
        module="lib/apk",
        finding=FindingEnum.F207,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_VULN_REGEX = MethodInfo(
        file_name="c_sharp",
        name="csharp_vuln_regular_expression",
        module="lib/root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L/E:P/RC:R",
        cwe_ids=["CWE-405"],
    )
    CS_REGEX_INJETCION = MethodInfo(
        file_name="c_sharp",
        name="csharp_regex_injection",
        module="lib/root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L/E:P/RC:R",
        cwe_ids=["CWE-405"],
    )
    KOTLIN_VULN_REGEX = MethodInfo(
        file_name="kotlin",
        name="kotlin_vuln_regex",
        module="lib/root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L/E:P/RC:R",
        cwe_ids=["CWE-405"],
    )
    JAVA_VULN_REGEX = MethodInfo(
        file_name="java",
        name="java_vuln_regex",
        module="lib/root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L/E:P/RC:R",
        cwe_ids=["CWE-405"],
    )
    JS_REGEX_INJETCION = MethodInfo(
        file_name="javascript",
        name="js_regex_injection",
        module="lib/root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L/E:P/RC:R",
        cwe_ids=["CWE-405"],
    )
    PYTHON_REGEX_DOS = MethodInfo(
        file_name="python",
        name="python_regex_dos",
        module="lib/root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L/E:P/RC:R",
        cwe_ids=["CWE-405"],
    )
    TS_REGEX_INJETCION = MethodInfo(
        file_name="typescript",
        name="ts_regex_injection",
        module="lib/root",
        finding=FindingEnum.F211,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:L/E:P/RC:R",
        cwe_ids=["CWE-405"],
    )
    JAVA_LEAK_STACKTRACE = MethodInfo(
        file_name="java",
        name="java_info_leak_stacktrace",
        module="lib/root",
        finding=FindingEnum.F234,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:R",
        cwe_ids=["CWE-209"],
    )
    TSCONFIG_SOURCEMAP_ENABLED = MethodInfo(
        file_name="conf_files",
        name="tsconfig_sourcemap_enabled",
        module="lib/root",
        finding=FindingEnum.F236,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U",
        cwe_ids=["CWE-200"],
    )
    JAVA_HAS_PRINT_STATEMENTS = MethodInfo(
        file_name="java",
        name="java_has_print_statements",
        module="lib/root",
        finding=FindingEnum.F237,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:C",
        cwe_ids=["CWE-200"],
    )
    DART_HAS_PRINT_STATEMENTS = MethodInfo(
        file_name="dart",
        name="dart_has_print_statements",
        module="lib/root",
        finding=FindingEnum.F237,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:C",
        cwe_ids=["CWE-200"],
    )
    PYTHON_HAS_PRINT_STATEMENTS = MethodInfo(
        file_name="python",
        name="python_has_print_statements",
        module="lib/root",
        finding=FindingEnum.F237,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N/E:U/RL:U/RC:C",
        cwe_ids=["CWE-200"],
    )
    DOTNETCONFIG_NOT_CUSTOM_ERRORS = MethodInfo(
        file_name="dotnetconfig",
        name="dotnetconfig_not_custom_errors",
        module="lib/path",
        finding=FindingEnum.F239,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CS_INFO_LEAK_ERRORS = MethodInfo(
        file_name="c_sharp",
        name="csharp_info_leak_errors",
        module="lib/root",
        finding=FindingEnum.F239,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:N/A:N",
        cwe_ids=["CWE-200"],
    )
    AWS_RDS_HAS_UNENCRYPTED_STORAGE = MethodInfo(
        file_name="aws",
        name="rds_has_unencrypted_storage",
        module="lib/dast",
        finding=FindingEnum.F246,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_RDS_UNENCRYPTED_STORAGE = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_has_unencrypted_storage",
        module="lib/root",
        finding=FindingEnum.F246,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U",
        cwe_ids=["CWE-311"],
    )
    TFM_RDS_UNENCRYPTED_STORAGE = MethodInfo(
        file_name="terraform",
        name="tfm_rds_has_unencrypted_storage",
        module="lib/root",
        finding=FindingEnum.F246,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U",
        cwe_ids=["CWE-311"],
    )
    AWS_EBS_IS_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="ebs_is_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TFM_EBS_UNENCRYPTED_VOLUMES = MethodInfo(
        file_name="terraform",
        name="tfm_ebs_unencrypted_volumes",
        module="lib/root",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-313"],
    )
    TFM_EC2_UNENCRYPTED_BLOCK_DEVICES = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_instance_unencrypted_ebs_block_devices",
        module="lib/root",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-313"],
    )
    TFM_EBS_UNENCRYPTED_DEFAULT = MethodInfo(
        file_name="terraform",
        name="tfm_ebs_unencrypted_by_default",
        module="lib/root",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-313"],
    )
    CFN_EC2_UNENCRYPTED_VOLUMES = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_unencrypted_volumes",
        module="lib/root",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-313"],
    )
    CFN_EC2_UNENCRYPTED_BLOCK_DEVICES = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_instance_unencrypted_ebs_block_devices",
        module="lib/root",
        finding=FindingEnum.F250,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-313"],
    )
    AWS_RDS_HAS_NOT_AUTOMATED_BACKUPS = MethodInfo(
        file_name="aws",
        name="rds_has_not_automated_backups",
        module="lib/dast",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_RDS_HAS_NOT_DELETION_PROTECTION = MethodInfo(
        file_name="aws",
        name="rds_has_not_deletion_protection",
        module="lib/dast",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_RDS_NOT_AUTO_BACKUPS = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_has_not_automated_backups",
        module="lib/root",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:U/C:N/I:H/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-463"],
    )
    CFN_RDS_NOT_TERMINATION_PROTEC = MethodInfo(
        file_name="cloudformation",
        name="cfn_rds_has_not_termination_protection",
        module="lib/root",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:U/C:N/I:H/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-463"],
    )
    CFN_DYNAMO_NOT_DEL_PROTEC = MethodInfo(
        file_name="cloudformation",
        name="cfn_dynamo_has_not_deletion_protection",
        module="lib/root",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:U/C:N/I:H/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-463"],
    )
    AWS_DYNAMODB_NOT_DEL_PROTEC = MethodInfo(
        file_name="aws",
        name="dynamodb_has_not_deletion_protection",
        module="lib/dast",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    TFM_DYNAMO_NOT_DEL_PROTEC = MethodInfo(
        file_name="terraform",
        name="tfm_dynamo_has_not_deletion_protection",
        module="lib/root",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:U/C:N/I:H/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-693"],
    )
    TFM_RDS_NO_DELETION_PROTEC = MethodInfo(
        file_name="terraform",
        name="tfm_rds_no_deletion_protection",
        module="lib/root",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:U/C:N/I:H/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-693"],
    )
    TFM_RDS_NOT_AUTO_BACKUPS = MethodInfo(
        file_name="terraform",
        name="tfm_rds_has_not_automated_backups",
        module="lib/root",
        finding=FindingEnum.F256,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:R/S:U/C:N/I:H/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-693"],
    )
    AWS_EC2_HAS_NOT_TERMINATION_PROTECTION = MethodInfo(
        file_name="aws",
        name="ec2_has_not_termination_protection",
        module="lib/dast",
        finding=FindingEnum.F257,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_EC2_NOT_TERMINATION_PROTEC = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_not_termination_protection",
        module="lib/root",
        finding=FindingEnum.F257,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
        cwe_ids=["CWE-463"],
    )
    EC2_NOT_TERMINATION_PROTEC = MethodInfo(
        file_name="terraform",
        name="ec2_has_not_termination_protection",
        module="lib/root",
        finding=FindingEnum.F257,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
        cwe_ids=["CWE-463"],
    )
    AWS_ELB2_HAS_NOT_DELETION_PROTECTION = MethodInfo(
        file_name="aws",
        name="elb2_has_not_deletion_protection",
        module="lib/dast",
        finding=FindingEnum.F258,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TFM_ELB2_NOT_DELETION_PROTEC = MethodInfo(
        file_name="terraform",
        name="tfm_elb2_has_not_deletion_protection",
        module="lib/root",
        finding=FindingEnum.F258,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
        cwe_ids=["CWE-463"],
    )
    CFN_ELB2_NOT_DELETION_PROTEC = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_has_not_deletion_protection",
        module="lib/root",
        finding=FindingEnum.F258,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
        cwe_ids=["CWE-463"],
    )
    AWS_DYNAMODB_HAS_NOT_POINT_IN_TIME_RECOVERY = MethodInfo(
        file_name="aws",
        name="dynamodb_has_not_point_in_time_recovery",
        module="lib/dast",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_NOT_POINT_TIME_RECOVERY = MethodInfo(
        file_name="cloudformation",
        name="cfn_has_not_point_in_time_recovery",
        module="lib/root",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-463"],
    )
    TFM_DB_NO_POINT_TIME_RECOVERY = MethodInfo(
        file_name="terraform",
        name="tfm_db_no_point_in_time_recovery",
        module="lib/root",
        finding=FindingEnum.F259,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-463"],
    )
    CONTAINER_WITHOUT_USER = MethodInfo(
        file_name="docker",
        name="container_without_user",
        module="lib/path",
        finding=FindingEnum.F266,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
    )
    CONTAINER_WITH_USER_ROOT = MethodInfo(
        file_name="docker",
        name="container_with_user_root",
        module="lib/path",
        finding=FindingEnum.F266,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    K8S_CHECK_ADD_CAPABILITY = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_add_capability",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_PRIVILEGE_ESCALATION_ENABLED = MethodInfo(
        file_name="kubernetes",
        name="k8s_allow_privilege_escalation_enabled",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_ROOT_CONTAINER = MethodInfo(
        file_name="kubernetes",
        name="k8s_root_container",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_ROOT_FILESYSTEM_READ_ONLY = MethodInfo(
        file_name="kubernetes",
        name="k8s_root_filesystem_read_only",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CHECK_RUN_AS_USER = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_run_as_user",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CHECK_SECCOMP_PROFILE = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_seccomp_profile",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CHECK_PRIVILEGED_USED = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_privileged_used",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CHECK_DROP_CAPABILITY = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_drop_capability",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CHECK_IF_CAPABILITY_EXISTS = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_if_capability_exists",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CHECK_IF_SYS_ADMIN_EXISTS = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_if_sys_admin_exists",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CONTAINER_WITHOUT_SECURITYCONTEXT = MethodInfo(
        file_name="kubernetes",
        name="k8s_container_without_securitycontext",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    K8S_CHECK_HOST_PID = MethodInfo(
        file_name="kubernetes",
        name="k8s_check_host_pid",
        module="lib/root",
        finding=FindingEnum.F267,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L/E:U/RL:O/RC:C",
        cwe_ids=["CWE-250"],
    )
    WEBVIEW_VULNS = MethodInfo(
        file_name="analyze_bytecodes",
        name="webview_vulnerabilities",
        module="lib/apk",
        finding=FindingEnum.F268,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_HAS_OLD_CREDS_ENABLED = MethodInfo(
        file_name="aws",
        name="have_old_creds_enabled",
        module="lib/dast",
        finding=FindingEnum.F277,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_HAS_OLD_SSH_PUBLIC_KEYS = MethodInfo(
        file_name="aws",
        name="has_old_ssh_public_keys",
        module="lib/dast",
        finding=FindingEnum.F277,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_HAS_OLD_ACCESS_KEYS = MethodInfo(
        file_name="aws",
        name="have_old_access_keys",
        module="lib/dast",
        finding=FindingEnum.F277,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TS_NON_SECURE_CONSTRUCTION_OF_COOKIES = MethodInfo(
        file_name="typescript",
        name="typescript_non_secure_construction_of_cookies",
        module="lib/root",
        finding=FindingEnum.F280,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-384"],
    )
    JS_NON_SECURE_CONSTRUCTION_OF_COOKIES = MethodInfo(
        file_name="javascript",
        name="javascript_non_secure_construction_of_cookies",
        module="lib/root",
        finding=FindingEnum.F280,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-384"],
    )
    PYTHON_SESSION_FIXATION = MethodInfo(
        file_name="python",
        name="python_session_fixation",
        module="lib/root",
        finding=FindingEnum.F280,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-384"],
    )
    AWS_S3_HAS_INSECURE_TRANSPORT = MethodInfo(
        file_name="aws",
        name="s3_has_insecure_transport",
        module="lib/dast",
        finding=FindingEnum.F281,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_BUCKET_POLICY_SEC_TRANSPORT = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_policy_has_secure_transport",
        module="lib/root",
        finding=FindingEnum.F281,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-311"],
    )
    TFM_BUCKET_POLICY_SEC_TRANSPORT = MethodInfo(
        file_name="terraform",
        name="tfm_bucket_policy_has_secure_transport",
        module="lib/root",
        finding=FindingEnum.F281,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-311"],
    )
    TS_SQL_INJECTION = MethodInfo(
        file_name="typescript",
        name="ts_sql_injection",
        module="lib/root",
        finding=FindingEnum.F297,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:R",
        cwe_ids=["CWE-89"],
    )
    JS_SQL_INJECTION = MethodInfo(
        file_name="javascript",
        name="js_sql_injection",
        module="lib/root",
        finding=FindingEnum.F297,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N/E:U/RL:X/RC:R",
        cwe_ids=["CWE-89"],
    )
    TFM_AZURE_APP_AUTH_OFF = MethodInfo(
        file_name="terraform",
        name="tfm_azure_app_authentication_off",
        module="lib/root",
        finding=FindingEnum.F300,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-284"],
    )
    TFM_AZURE_CLIENT_CERT_ENABLED = MethodInfo(
        file_name="terraform",
        name="tfm_azure_as_client_certificates_enabled",
        module="lib/root",
        finding=FindingEnum.F300,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-284"],
    )
    JS_INSECURE_JWT_TOKEN = MethodInfo(
        file_name="javascript",
        name="js_uses_insecure_jwt_token",
        module="lib/root",
        finding=FindingEnum.F309,
        developer=DeveloperEnum.FLOR_CALDERON,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-287"],
    )
    TS_INSECURE_JWT_TOKEN = MethodInfo(
        file_name="typescript",
        name="ts_insecure_jwt_token",
        module="lib/root",
        finding=FindingEnum.F309,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-287"],
    )
    IMPROPER_CERTIFICATE_VALIDATION = MethodInfo(
        file_name="analyze_bytecodes",
        name="improper_certificate_validation",
        module="lib/apk",
        finding=FindingEnum.F313,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    PYTHON_UNSAFE_CERTIFICATE_VALIDATION = MethodInfo(
        file_name="python",
        name="python_unsafe_certificate_validation",
        module="lib/root",
        finding=FindingEnum.F313,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-295"],
    )
    CFN_INSECURE_CERTIFICATE = MethodInfo(
        file_name="cloudformation",
        name="cfn_unsafe_certificate",
        module="lib/root",
        finding=FindingEnum.F313,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-295"],
    )
    CS_LDAP_CONN_AUTH = MethodInfo(
        file_name="c_sharp",
        name="csharp_ldap_connections_authenticated",
        module="lib/root",
        finding=FindingEnum.F320,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-90"],
    )
    PYTHON_LDAP_CONN_AUTH = MethodInfo(
        file_name="python",
        name="python_unsafe_ldap_connections",
        module="lib/root",
        finding=FindingEnum.F320,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-90"],
    )
    AWS_IAM_HAS_PRIVILEGES_OVER_IAM = MethodInfo(
        file_name="aws",
        name="iam_has_privileges_over_iam",
        module="lib/dast",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_KMS_HAS_MASTER_KEYS_EXPOSED_TO_EVERYONE = MethodInfo(
        file_name="aws",
        name="kms_has_master_keys_exposed_to_everyone",
        module="lib/dast",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_HAS_WILDCARD_RESOURCE_IN_WRITE_ACTION = MethodInfo(
        file_name="aws",
        name="iam_has_wildcard_resource_on_write_action",
        module="lib/dast",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_IS_POLICY_MISS_CONFIGURED = MethodInfo(
        file_name="aws",
        name="iam_is_policy_miss_configured",
        module="lib/dast",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CFN_PERMISSIVE_POLICY = MethodInfo(
        file_name="cloudformation",
        name="cfn_permissive_policy",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    TFM_PERMISSIVE_POLICY = MethodInfo(
        file_name="terraform",
        name="terraform_permissive_policy",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    CFN_KMS_MASTER_KEYS_EXPOSED = MethodInfo(
        file_name="cloudformation",
        name="cfn_kms_key_has_master_keys_exposed_to_everyone",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    CFN_IAM_WILDCARD_WRITE = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_has_wildcard_resource_on_write_action",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    TFM_IAM_WILDCARD_WRITE = MethodInfo(
        file_name="terraform",
        name="tfm_iam_has_wildcard_resource_on_write_action",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    TFM_KMS_MASTER_KEYS_EXPOSED = MethodInfo(
        file_name="terraform",
        name="tfm_kms_key_has_master_keys_exposed_to_everyone",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    CFN_IAM_PERMISSIONS_POLICY_WILDCARD_RESOURCES = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_permissions_policy_wildcard_resources",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    CFN_IAM_PERMISSIONS_POLICY_WILDCARD_ACTIONS = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_permissions_policy_wildcard_actions",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    CFN_IAM_TRUST_POLICY_WILDCARD_ACTION = MethodInfo(
        file_name="cloudformation",
        name="cfn_iam_trust_policy_allow_wildcard_action",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    TFM_IAM_TRUST_POLICY_WILDCARD_ACTION = MethodInfo(
        file_name="terraform",
        name="tfm_iam_trust_policy_allow_wildcard_action",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    JSON_PRINCIPAL_WILDCARD = MethodInfo(
        file_name="conf_files",
        name="json_principal_wildcard",
        module="lib/root",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    DOTNETCONFIG_EXCESSIVE_AUTH_PRIVILEGES = MethodInfo(
        file_name="dotnetconfig",
        name="dotnetconfig_excessive_auth_privileges",
        module="lib/path",
        finding=FindingEnum.F325,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L/E:U/RL:U/RC:C",
        cwe_ids=["CWE-250"],
    )
    KUBERNETES_INSECURE_PORT = MethodInfo(
        file_name="kubernetes",
        name="kubernetes_insecure_port",
        module="lib/root",
        finding=FindingEnum.F332,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-319"],
    )
    KUBERNETES_USES_HTTP = MethodInfo(
        file_name="kubernetes",
        name="kubernetes_insecure_http_channel",
        module="lib/root",
        finding=FindingEnum.F332,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-319"],
    )
    CONTAINER_DISABLED_SSL = MethodInfo(
        file_name="docker",
        name="docker_disabled_ssl",
        module="lib/path",
        finding=FindingEnum.F332,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
    )
    CFN_AWS_SEC_GROUP_USING_TCP = MethodInfo(
        file_name="cloudformation",
        name="cfn_aws_sec_group_using_tcp",
        module="lib/root",
        finding=FindingEnum.F332,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-319"],
    )
    TFM_AWS_SEC_GROUP_USING_TCP = MethodInfo(
        file_name="terraform",
        name="tfm_aws_sec_group_using_tcp",
        module="lib/root",
        finding=FindingEnum.F332,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-319"],
    )
    KT_UNENCRYPTED_CHANNEL = MethodInfo(
        file_name="kotlin",
        name="kotlin_unencrypted_channel",
        module="lib/root",
        finding=FindingEnum.F332,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-319"],
    )
    CFN_SERVER_SSL_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_server_ssl_disabled",
        module="lib/root",
        finding=FindingEnum.F332,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:A/AC:L/PR:N/UI:R/S:U/C:L/I:N/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-319"],
    )
    AWS_EC2_HAS_TERMINATE_SHUTDOWN_BEHAVIOR = MethodInfo(
        file_name="aws",
        name="ec2_has_terminate_shutdown_behavior",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_HAS_UNUSED_SEGGROUPS = MethodInfo(
        file_name="aws",
        name="has_unused_seggroups",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_HAS_ASSOCIATE_PUBLIC_IP_ADDRESS = MethodInfo(
        file_name="aws",
        name="ec2_has_associate_public_ip_address",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_IAM_INSTANCE_WITHOUT_PROFILE = MethodInfo(
        file_name="aws",
        name="ec2_iam_instances_without_profile",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_HAS_DEFINED_USER_DATA = MethodInfo(
        file_name="aws",
        name="has_defined_user_data",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_HAS_INSTANCES_USING_UNAPPROVED_AMIS = MethodInfo(
        file_name="aws",
        name="has_instances_using_unapproved_amis",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_HAS_UNUSED_KEY_PAIRS = MethodInfo(
        file_name="aws",
        name="has_unused_ec2_key_pairs",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_HAS_PUBLICLY_SHARED_AMIS = MethodInfo(
        file_name="aws",
        name="has_publicly_shared_amis",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_HAS_UNENCRYPTED_SNAPSHOTS = MethodInfo(
        file_name="aws",
        name="has_unencrypted_snapshots",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EC2_HAS_UNENCRYPTED_AMIS = MethodInfo(
        file_name="aws",
        name="has_unencrypted_amis",
        module="lib/dast",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_EC2_NO_IAM = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_not_an_iam_instance_profile",
        module="lib/root",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-16"],
    )
    CFN_EC2_ASSOC_PUB_IP = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_associate_public_ip_address",
        module="lib/root",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-16"],
    )
    CFN_EC2_TERMINATE_SHUTDOWN_BEHAVIOR = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_has_terminate_shutdown_behavior",
        module="lib/root",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-16"],
    )
    TFM_EC2_NO_IAM = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_not_an_iam_instance_profile",
        module="lib/root",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-16"],
    )
    EC2_TERMINATE_SHUTDOWN_BEHAVIOR = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_has_terminate_shutdown_behavior",
        module="lib/root",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-16"],
    )
    TFM_EC2_ASSOC_PUB_IP = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_associate_public_ip_address",
        module="lib/root",
        finding=FindingEnum.F333,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-16"],
    )
    AWS_S3_BUCKET_VERSIONING_DISABLED = MethodInfo(
        file_name="aws",
        name="s3_bucket_versioning_disabled",
        module="lib/dast",
        finding=FindingEnum.F335,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CFN_S3_VERSIONING_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_s3_bucket_versioning_disabled",
        module="lib/root",
        finding=FindingEnum.F335,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-922"],
    )
    TFM_S3_VERSIONING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_s3_bucket_versioning_disabled",
        module="lib/root",
        finding=FindingEnum.F335,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:X",
        cwe_ids=["CWE-922"],
    )
    JS_SALT_IS_HARDCODED = MethodInfo(
        file_name="javascript",
        name="js_salt_is_harcoded",
        module="lib/root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O",
        cwe_ids=["CWE-749"],
    )
    TS_SALT_IS_HARDCODED = MethodInfo(
        file_name="typescript",
        name="ts_salt_is_harcoded",
        module="lib/root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O",
        cwe_ids=["CWE-749"],
    )
    JAVA_SALT_IS_HARDCODED = MethodInfo(
        file_name="java",
        name="java_salt_is_harcoded",
        module="lib/root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O",
        cwe_ids=["CWE-749"],
    )
    KOTLIN_SALT_IS_HARDCODED = MethodInfo(
        file_name="kotlin",
        name="kotlin_salt_is_hardcoded",
        module="lib/root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O",
        cwe_ids=["CWE-749"],
    )
    GO_SALT_IS_HARDCODED = MethodInfo(
        file_name="go",
        name="go_salt_is_hardcoded",
        module="lib/root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O",
        cwe_ids=["CWE-749"],
    )
    DART_SALT_IS_HARDCODED = MethodInfo(
        file_name="dart",
        name="dart_salt_is_hardcoded",
        module="lib/root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O",
        cwe_ids=["CWE-749"],
    )
    CS_CHECK_HASHES_SALT = MethodInfo(
        file_name="c_sharp",
        name="csharp_check_hashes_salt",
        module="lib/root",
        finding=FindingEnum.F338,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O",
        cwe_ids=["CWE-749"],
    )
    JS_INSECURE_COMPRESSION_ALGORITHM = MethodInfo(
        file_name="javascript",
        name="javascript_insecure_compression_algorithm",
        module="lib/root",
        finding=FindingEnum.F343,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:W/RC:R",
        cwe_ids=["CWE-444"],
    )
    TS_INSECURE_COMPRESSION_ALGORITHM = MethodInfo(
        file_name="typescript",
        name="typescript_insecure_compression_algorithm",
        module="lib/root",
        finding=FindingEnum.F343,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:W/RC:R",
        cwe_ids=["CWE-444"],
    )
    JS_LOCAL_STORAGE_WITH_SENSITIVE_DATA = MethodInfo(
        file_name="javascript",
        name="javascript_local_storage_with_sensitive_data",
        module="lib/root",
        finding=FindingEnum.F344,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L/E:U/RL:X/RC:U",
        cwe_ids=["CWE-922"],
    )
    TS_LOCAL_STORAGE_WITH_SENSITIVE_DATA = MethodInfo(
        file_name="typescript",
        name="typescript_local_storage_with_sensitive_data",
        module="lib/root",
        finding=FindingEnum.F344,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L/E:U/RL:X/RC:U",
        cwe_ids=["CWE-922"],
    )
    JS_LOCAL_STORAGE_SENS_DATA_ASSIGNMENT = MethodInfo(
        file_name="javascript",
        name="javascript_local_storage_sensitive_data_async",
        module="lib/root",
        finding=FindingEnum.F344,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L/E:U/RL:X/RC:U",
        cwe_ids=["CWE-922"],
    )
    TS_LOCAL_STORAGE_SENS_DATA_ASSIGNMENT = MethodInfo(
        file_name="typescript",
        name="typescript_local_storage_sensitive_data_assignment",
        module="lib/root",
        finding=FindingEnum.F344,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:H/A:L/E:U/RL:X/RC:U",
        cwe_ids=["CWE-922"],
    )
    DANGEROUS_PERMISSIONS = MethodInfo(
        file_name="android",
        name="has_dangerous_permissions",
        module="lib/path",
        finding=FindingEnum.F346,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    JAVA_INSECURE_TRUST_MANAGER = MethodInfo(
        file_name="java",
        name="java_use_insecure_trust_manager",
        module="lib/root",
        finding=FindingEnum.F350,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-310"],
    )
    JS_DECODE_INSECURE_JWT_TOKEN = MethodInfo(
        file_name="javascript",
        name="js_decode_insecure_jwt_token",
        module="lib/root",
        finding=FindingEnum.F353,
        developer=DeveloperEnum.FLOR_CALDERON,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:U/RC:C",
        cwe_ids=["CWE-287"],
    )
    TS_DECODE_INSECURE_JWT_TOKEN = MethodInfo(
        file_name="typescript",
        name="ts_decode_insecure_jwt_token",
        module="lib/root",
        finding=FindingEnum.F353,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.EXTERNAL,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:U/RC:C",
        cwe_ids=["CWE-287"],
    )
    JAVA_UPLOAD_SIZE_LIMIT = MethodInfo(
        file_name="java",
        name="java_upload_size_limit",
        module="lib/root",
        finding=FindingEnum.F354,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RC:R",
        cwe_ids=["CWE-770"],
    )
    CS_CERT_VALIDATION_DISABLED = MethodInfo(
        file_name="c_sharp",
        name="csharp_cert_validation_disabled",
        module="lib/root",
        finding=FindingEnum.F358,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:R/S:U/C:L/I:L/A:N/E:P/RL:O/RC:R",
        cwe_ids=["CWE-295"],
    )
    AWS_IAM_NOT_REQUIRES_UPPERCASE = MethodInfo(
        file_name="aws",
        name="not_requires_uppercase",
        module="lib/dast",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_NOT_REQUIRES_LOWERCASE = MethodInfo(
        file_name="aws",
        name="not_requires_lowercase",
        module="lib/dast",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_NOT_REQUIRES_SYMBOLS = MethodInfo(
        file_name="aws",
        name="not_requires_symbols",
        module="lib/dast",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_NOT_REQUIRES_NUMBERS = MethodInfo(
        file_name="aws",
        name="not_requires_numbers",
        module="lib/dast",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_MIN_PASSWORD_LEN_UNSAFE = MethodInfo(
        file_name="aws",
        name="min_password_len_unsafe",
        module="lib/dast",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_PASSWORD_REUSE_UNSAFE = MethodInfo(
        file_name="aws",
        name="password_reuse_unsafe",
        module="lib/dast",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_IAM_PASSWORD_EXPIRATION_UNSAFE = MethodInfo(
        file_name="aws",
        name="password_expiration_unsafe",
        module="lib/dast",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    CFN_INSEC_GEN_SECRET = MethodInfo(
        file_name="cloudformation",
        name="cfn_insecure_generate_secret_string",
        module="lib/root",
        finding=FindingEnum.F363,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:L/E:U/RL:X/RC:X",
        cwe_ids=["CWE-521"],
    )
    CS_CONFLICTING_ANNOTATIONS = MethodInfo(
        file_name="c_sharp",
        name="csharp_conflicting_annotations",
        module="lib/root",
        finding=FindingEnum.F366,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:L/E:U/RL:U/RC:R",
        cwe_ids=["CWE-749"],
    )
    JAVA_HOST_KEY_CHECKING = MethodInfo(
        file_name="java",
        name="java_host_key_checking",
        module="lib/root",
        finding=FindingEnum.F368,
        developer=DeveloperEnum.FABIO_LAGOS,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N/E:U/RL:O/RC:U",
        cwe_ids=["CWE-923"],
    )
    JS_USES_INNERHTML = MethodInfo(
        file_name="javascript",
        name="js_uses_innerhtml",
        module="lib/root",
        finding=FindingEnum.F371,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-79"],
    )
    TS_USES_INNERHTML = MethodInfo(
        file_name="typescript",
        name="ts_uses_innerhtml",
        module="lib/root",
        finding=FindingEnum.F371,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-79"],
    )
    JS_USES_BYPASS_SECURITY_TRUST_URL = MethodInfo(
        file_name="javascript",
        name="js_use_of_bypass_security_trust_url",
        module="lib/root",
        finding=FindingEnum.F371,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-79"],
    )
    TS_USES_BYPASS_SECURITY_TRUST_URL = MethodInfo(
        file_name="typescript",
        name="ts_use_of_bypass_security_trust_url",
        module="lib/root",
        finding=FindingEnum.F371,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-79"],
    )
    JS_USES_DANGEROUSLY_SET_HTML = MethodInfo(
        file_name="javascript",
        name="js_uses_dangerously_set_html",
        module="lib/root",
        finding=FindingEnum.F371,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-79"],
    )
    TS_USES_DANGEROUSLY_SET_HTML = MethodInfo(
        file_name="typescript",
        name="ts_uses_dangerously_set_html",
        module="lib/root",
        finding=FindingEnum.F371,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N/E:U/RL:X/RC:X",
        cwe_ids=["CWE-79"],
    )
    AWS_ELB2_HAS_NOT_HTTPS = MethodInfo(
        file_name="aws",
        name="elbv2_listeners_not_using_https",
        module="lib/dast",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_CFT_SERVES_CONTENT_OVER_HTTP = MethodInfo(
        file_name="aws",
        name="cft_serves_content_over_http",
        module="lib/dast",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    JSON_HTTPS_FLAG_MISSING = MethodInfo(
        file_name="conf_files",
        name="json_https_flag_missing",
        module="lib/root",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.JULIAN_GOMEZ,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-650"],
    )
    CFN_CONTENT_HTTP = MethodInfo(
        file_name="cloudformation",
        name="cfn_serves_content_over_http",
        module="lib/root",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-650"],
    )
    TFM_CONTENT_HTTP = MethodInfo(
        file_name="terraform",
        name="tfm_serves_content_over_http",
        module="lib/root",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-650"],
    )
    CFN_ELB2_INSEC_PROTO = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_uses_insecure_protocol",
        module="lib/root",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.ANDRES_CUBEROS,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-319"],
    )
    TFM_ELB2_INSEC_PROTO = MethodInfo(
        file_name="terraform",
        name="tfm_elb2_uses_insecure_protocol",
        module="lib/root",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-650"],
    )
    TFM_AZURE_KV_ONLY_ACCESS_HTTPS = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_only_accessible_over_https",
        module="lib/root",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-650"],
    )
    TFM_AZURE_SA_INSEC_TRANSFER = MethodInfo(
        file_name="terraform",
        name="tfm_azure_sa_insecure_transfer",
        module="lib/root",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-650"],
    )
    USES_HTTP_RESOURCES = MethodInfo(
        file_name="analyze_bytecodes",
        name="uses_http_resources",
        module="lib/apk",
        finding=FindingEnum.F372,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:A/AC:H/PR:N/UI:R/S:U/C:L/I:L/A:N/E:U/RL:O/RC:X",
        cwe_ids=["CWE-650"],
    )
    TS_UNNECESSARY_IMPORTS = MethodInfo(
        file_name="typescript",
        name="ts_unnecessary_imports",
        module="lib/root",
        finding=FindingEnum.F379,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L/E:U/RL:X/RC:R",
        cwe_ids=["CWE-650"],
    )
    JS_UNNECESSARY_IMPORTS = MethodInfo(
        file_name="javascript",
        name="js_unnecessary_imports",
        module="lib/root",
        finding=FindingEnum.F379,
        developer=DeveloperEnum.JHON_ROMERO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.HACKER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L/E:U/RL:X/RC:R",
        cwe_ids=["CWE-650"],
    )
    UNPINNED_DOCKER_IMAGE = MethodInfo(
        file_name="docker",
        name="unpinned_docker_image",
        module="lib/path",
        finding=FindingEnum.F380,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    BASH_IMAGE_HAS_DIGEST = MethodInfo(
        file_name="bash",
        name="bash_image_has_digest",
        module="lib/path",
        finding=FindingEnum.F380,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    DOCKER_COMPOSE_IMAGE_HAS_DIGEST = MethodInfo(
        file_name="docker_compose",
        name="docker_compose_image_has_digest",
        module="lib/root",
        finding=FindingEnum.F380,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-749"],
    )
    CHECK_REQUIRED_VERSION = MethodInfo(
        file_name="terraform",
        name="check_required_version",
        module="lib/root",
        finding=FindingEnum.F381,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-437"],
    )
    COMPOSER_JSON_DEV = MethodInfo(
        file_name="composer",
        name="composer_json_dev",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    COMPOSER_LOCK_DEV = MethodInfo(
        file_name="composer",
        name="composer_lock_dev",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CONAN_CONANFILE_PY_DEV = MethodInfo(
        file_name="python_config_files",
        name="conan_conanfile_py_dev",
        module="lib/root",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CONAN_CONANFILE_TXT_DEV = MethodInfo(
        file_name="conan",
        name="conan_conanfile_txt_dev",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CONAN_LOCK_DEV = MethodInfo(
        file_name="conan",
        name="conan_lock_dev",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    GEM_GEMFILE_DEV = MethodInfo(
        file_name="gem",
        name="gem_gemfile_dev",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    NPM_PKG_JSON = MethodInfo(
        file_name="npm",
        name="npm_pkg_json",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    NPM_PKG_LOCK_JSON = MethodInfo(
        file_name="npm",
        name="npm_pkg_lock_json",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.DEFAULT,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.ASSERTS,
    )
    NPM_YARN_LOCK_DEV = MethodInfo(
        file_name="npm",
        name="npm_yarn_lock_dev",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    PUB_PUBSPEC_YAML_DEV = MethodInfo(
        file_name="pub",
        name="pub_pubspec_yaml_dev",
        module="lib/sca",
        finding=FindingEnum.F393,
        developer=DeveloperEnum.LEWIS_CONTRERAS,
        technique=TechniqueEnum.SCA,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_CLOUDTRAIL_FILES_NOT_VALIDATED = MethodInfo(
        file_name="aws",
        name="cloudtrail_files_not_validated",
        module="lib/dast",
        finding=FindingEnum.F394,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    TFM_CTRAIL_LOG_NOT_VALIDATED = MethodInfo(
        file_name="terraform",
        name="tfm_aws_s3_versioning_disabled",
        module="lib/root",
        finding=FindingEnum.F394,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-117"],
    )
    CFN_LOG_NOT_VALIDATED = MethodInfo(
        file_name="cloudformation",
        name="cfn_log_files_not_validated",
        module="lib/root",
        finding=FindingEnum.F394,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-117"],
    )
    AWS_KMS_IS_KEY_ROTATION_DISABLED = MethodInfo(
        file_name="aws",
        name="kms_key_is_key_rotation_absent_or_disabled",
        module="lib/dast",
        finding=FindingEnum.F396,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_SECRETS_HAS_AUTOMATIC_ROTATION_DISABLED = MethodInfo(
        file_name="aws",
        name="secrets_manager_has_automatic_rotation_disabled",
        module="lib/dast",
        finding=FindingEnum.F396,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TFM_KMS_KEY_ROTATION_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_kms_key_is_key_rotation_absent_or_disabled",
        module="lib/root",
        finding=FindingEnum.F396,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-255"],
    )
    CFN_KMS_KEY_ROTATION_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_kms_key_is_key_rotation_absent_or_disabled",
        module="lib/root",
        finding=FindingEnum.F396,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-255"],
    )
    FRAGMENT_INJECTION = MethodInfo(
        file_name="analyze_bytecodes",
        name="has_fragment_injection",
        module="lib/apk",
        finding=FindingEnum.F398,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.APK,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_ELBV2_HAS_ACCESS_LOGGING_DISABLED = MethodInfo(
        file_name="aws",
        name="elbv2_has_access_logging_disabled",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_EKS_HAS_DISABLED_CLUSTER_LOGGING = MethodInfo(
        file_name="aws",
        name="eks_has_disable_cluster_logging",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_CLOUDFRONT_HAS_LOGGING_DISABLED = MethodInfo(
        file_name="aws",
        name="cloudfront_has_logging_disabled",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_CLOUDTRAIL_TRAILS_NOT_MULTIREGION = MethodInfo(
        file_name="aws",
        name="cloudtrail_trails_not_multiregion",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_IS_TRAIL_BUCKET_LOGGING_DISABLED = MethodInfo(
        file_name="aws",
        name="is_trail_bucket_logging_disabled",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_S3_HAS_ACCESS_LOGGING_DISABLED = MethodInfo(
        file_name="aws",
        name="s3_has_server_access_logging_disabled",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_EC2_MONITORING_DISABLED = MethodInfo(
        file_name="aws",
        name="ec2_monitoring_disabled",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_CF_DISTRIBUTION_HAS_LOGGING_DISABLED = MethodInfo(
        file_name="aws",
        name="cf_distribution_has_logging_disabled",
        module="lib/dast",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CFN_LOG_CONF_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_bucket_has_logging_conf_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    CFN_ELB_ACCESS_LOG_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb_has_access_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    CFN_CF_DISTR_LOG_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_cf_distribution_has_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    CFN_TRAILS_NOT_MULTIREGION = MethodInfo(
        file_name="cloudformation",
        name="cfn_trails_not_multiregion",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    CFN_EC2_MONITORING_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_ec2_monitoring_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    CFN_ELB2_LOGS_S3_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_elb2_has_access_logs_s3_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    TFM_ELB_LOGGING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_elb_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    TFM_EC2_MONITORING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_ec2_monitoring_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    TFM_CF_DISTR_LOG_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_distribution_has_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    TFM_TRAILS_NOT_MULTIREGION = MethodInfo(
        file_name="terraform",
        name="tfm_trails_not_multiregion",
        module="lib/root",
        finding=FindingEnum.F400,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    TFM_AZURE_KV_SECRET_NO_EXPIRATION = MethodInfo(
        file_name="terraform",
        name="tfm_azure_kv_secret_no_expiration_date",
        module="lib/root",
        finding=FindingEnum.F401,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:H/I:N/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-521"],
    )
    TFM_AZURE_STORAGE_LOG_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_azure_storage_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F402,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-778"],
    )
    TFM_AZURE_APP_LOG_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_azure_app_service_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F402,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-778"],
    )
    TFM_AZURE_SQL_LOG_RETENT = MethodInfo(
        file_name="terraform",
        name="tfm_azure_sql_server_audit_log_retention",
        module="lib/root",
        finding=FindingEnum.F402,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-778"],
    )
    XML_INSECURE_CONFIGURATION = MethodInfo(
        file_name="conf_files",
        name="xml_insecure_configuration",
        module="lib/path",
        finding=FindingEnum.F403,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    BASH_EXCESSIVE_PRIVILEGES_FOR_OTHERS = MethodInfo(
        file_name="bash",
        name="excessive_privileges_for_others",
        module="lib/path",
        finding=FindingEnum.F405,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_EFS_IS_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="efs_is_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F406,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CFN_AWS_EFS_UNENCRYPTED = MethodInfo(
        file_name="cloudformation",
        name="cfn_aws_efs_unencrypted",
        module="lib/root",
        finding=FindingEnum.F406,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    TFM_AWS_EFS_UNENCRYPTED = MethodInfo(
        file_name="terraform",
        name="tfm_aws_efs_unencrypted",
        module="lib/root",
        finding=FindingEnum.F406,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    AWS_EBS_HAS_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="ebs_has_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F407,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    CFN_AWS_EBS_VOLUMES_UNENCRYPTED = MethodInfo(
        file_name="cloudformation",
        name="cfn_aws_ebs_volumes_unencrypted",
        module="lib/root",
        finding=FindingEnum.F407,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    TFM_AWS_EBS_VOLUMES_UNENCRYPTED = MethodInfo(
        file_name="terraform",
        name="tfm_aws_ebs_volumes_unencrypted",
        module="lib/root",
        finding=FindingEnum.F407,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    CFN_API_GATEWAY_LOGGING_DISABLED = MethodInfo(
        file_name="cloudformation",
        name="cfn_api_gateway_access_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F408,
        developer=DeveloperEnum.ALEJANDRO_TRUJILLO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    TFM_API_GATEWAY_LOGGING_DISABLED = MethodInfo(
        file_name="terraform",
        name="tfm_api_gateway_access_logging_disabled",
        module="lib/root",
        finding=FindingEnum.F408,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-778"],
    )
    AWS_EBS_USES_DEFAULT_KMS_KEY = MethodInfo(
        file_name="aws",
        name="ebs_uses_default_kms_key",
        module="lib/dast",
        finding=FindingEnum.F411,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_REDSHIFT_USES_DEFAULT_KMS_KEY = MethodInfo(
        file_name="aws",
        name="redshift_uses_default_kms_key",
        module="lib/dast",
        finding=FindingEnum.F411,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_EFS_USES_DEFAULT_KMS_KEY = MethodInfo(
        file_name="aws",
        name="efs_uses_default_kms_key",
        module="lib/dast",
        finding=FindingEnum.F411,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    AWS_FSX_USES_DEFAULT_KMS_KEY = MethodInfo(
        file_name="aws",
        name="fsx_uses_default_kms_key",
        module="lib/dast",
        finding=FindingEnum.F411,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
    TFM_AZURE_KEY_VAULT_NOT_RECOVER = MethodInfo(
        file_name="terraform",
        name="tfm_azure_key_vault_not_recoverable",
        module="lib/root",
        finding=FindingEnum.F412,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:N/A:H/E:U/RL:O/RC:C",
        cwe_ids=["CWE-463"],
    )
    CS_INSECURE_ASSEMBLY_LOAD = MethodInfo(
        file_name="c_sharp",
        name="csharp_insecure_assembly_load",
        module="lib/root",
        finding=FindingEnum.F413,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:L/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N/E:P/RL:U/RC:C",
        cwe_ids=["CWE-434"],
    )
    CS_DISABLED_HTTP_HEADER_CHECK = MethodInfo(
        file_name="c_sharp",
        name="csharp_disabled_http_header_check",
        module="lib/root",
        finding=FindingEnum.F414,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:P/RL:O/RC:C",
        cwe_ids=["CWE-644"],
    )
    CS_XAML_INJECTION = MethodInfo(
        file_name="c_sharp",
        name="csharp_xaml_injection",
        module="lib/root",
        finding=FindingEnum.F416,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.ADVANCE_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:P/RL:U/RC:C",
        cwe_ids=["CWE-94"],
    )
    DOCKER_COMPOSE_READ_ONLY = MethodInfo(
        file_name="docker_compose",
        name="docker_compose_read_only",
        module="lib/root",
        finding=FindingEnum.F418,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    DOCKER_USING_ADD_COMMAND = MethodInfo(
        file_name="docker",
        name="docker_using_add_command",
        module="lib/path",
        finding=FindingEnum.F418,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ARM,
        cvss="CVSS:3.1/AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N/E:U/RL:O/RC:C",
        cwe_ids=["CWE-16"],
    )
    JAVA_USES_SYSTEM_EXIT = MethodInfo(
        file_name="java",
        name="java_uses_exit_method",
        module="lib/root",
        finding=FindingEnum.F423,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.ASSERTS,
        cvss="CVSS:3.1/AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:L/E:U/RL:U/RC:R",
        cwe_ids=["CWE-382"],
    )
    K8S_IMAGE_HAS_DIGEST = MethodInfo(
        file_name="kubernetes",
        name="k8s_image_has_digest",
        module="lib/root",
        finding=FindingEnum.F426,
        developer=DeveloperEnum.LUIS_PATINO,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
        cvss="CVSS:3.1/AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N/E:U/RL:O/RC:R",
        cwe_ids=["CWE-749"],
    )
    DOCKER_PORT_EXPOSED = MethodInfo(
        file_name="docker",
        name="docker_port_exposed",
        module="lib/path",
        finding=FindingEnum.F427,
        developer=DeveloperEnum.JUAN_ECHEVERRI,
        technique=TechniqueEnum.BASIC_SAST,
        origin=MethodOriginEnum.DEVELOPER,
    )
    AWS_REDSHIFT_HAS_ENCRYPTION_DISABLED = MethodInfo(
        file_name="aws",
        name="redshift_has_encryption_disabled",
        module="lib/dast",
        finding=FindingEnum.F433,
        developer=DeveloperEnum.LUIS_SAAVEDRA,
        technique=TechniqueEnum.DAST,
        origin=MethodOriginEnum.ASSERTS,
    )
