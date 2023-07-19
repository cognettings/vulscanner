SERVICE_ATTRIBUTES: dict[str, set[str]] = dict(
    continuous={
        "is_continuous",
    },
    request_zero_risk={"can_request_zero_risk"},
    service_black={
        "has_service_black",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    service_white={
        "has_service_white",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    report_vulnerabilities={"can_report_vulnerabilities"},
    forces={
        "has_forces",
        "is_fluidattacks_customer",
        "must_only_have_fluidattacks_hackers",
    },
    asm={
        "has_asm",
    },
    squad={
        "has_squad",
    },
)

SERVICE_ATTRIBUTES_SET: set[str] = {
    action for actions in SERVICE_ATTRIBUTES.values() for action in actions
}
