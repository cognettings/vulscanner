from typing import (
    NamedTuple,
)

# Containers
_SCALE = NamedTuple(
    "_SCALE",
    [
        ("more_passive", str),
        ("optional_passive", str),
        ("passive", str),
        ("neutral", str),
        ("agressive", str),
        ("optional_agressive", str),
        ("more_agressive", str),
    ],
)


# https://coolors.co/33cc99-1e8c7d-084c61-177e89-ffc857-ed7340-da1e28
RISK = _SCALE(
    more_passive="#33cc99",
    optional_passive="#1e8c7d",
    passive="#084c61",
    neutral="#177e89",
    agressive="#ffc857",
    optional_agressive="#ed7340",
    more_agressive="#da1e28",
)

# https://coolors.co/fdd25e-fecf49-ffcc33-f8903a-f77d26-f67014-f46201
TREATMENT = _SCALE(
    more_passive="#fdd25e",
    optional_passive="#fecf49",
    passive="#ffcc33",
    neutral="#f8903a",
    agressive="#f77d26",
    optional_agressive="#f67014",
    more_agressive="#f46201",
)

# https://coolors.co/abb8b6-97a8a5-839794-6f8683-657e7b-607a77-5b7572
OTHER = _SCALE(
    more_passive="#abb8b6",
    optional_passive="#97a8a5",
    passive="#839794",
    neutral="#6f8683",
    agressive="#657e7b",
    optional_agressive="#607a77",
    more_agressive="#5b7572",
)

GRAY_JET: str = "#323031"
EXPOSURE: str = "#ac0a17"
VULNERABILITIES_COUNT: str = "#cc6699"
TYPES_COUNT: str = "#7f0540"
OTHER_COUNT: str = "#fda6ab"
