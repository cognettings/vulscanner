from typing import (
    cast,
)
from unreliable_indicators.enums import (
    Entity,
    EntityAttr,
    EntityDependency,
    EntityId,
)
from unreliable_indicators.types import (
    EntityToUpdate,
)

# Constants
ENTITIES = {
    Entity.event: dict(
        args={
            EntityId.ids,
        },
        attrs={
            EntityAttr.solving_date: dict(
                dependencies={
                    EntityDependency.solve_event,
                }
            ),
        },
    ),
    Entity.finding: dict(
        args={
            EntityId.ids,
        },
        attrs={
            EntityAttr.closed_vulnerabilities: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                }
            ),
            EntityAttr.max_open_severity_score: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                }
            ),
            EntityAttr.newest_vulnerability_report_date: dict(
                dependencies={
                    EntityDependency.approve_draft,
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.oldest_open_vulnerability_report_date: dict(
                dependencies={
                    EntityDependency.approve_draft,
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.oldest_vulnerability_report_date: dict(
                dependencies={
                    EntityDependency.approve_draft,
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.open_vulnerabilities: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                }
            ),
            EntityAttr.rejected_vulnerabilities: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                }
            ),
            EntityAttr.status: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                }
            ),
            EntityAttr.submitted_vulnerabilities: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                }
            ),
            EntityAttr.total_open_cvssf: dict(
                dependencies={
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.update_severity,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.treatment_summary: dict(
                dependencies={
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.deactivate_root,
                    EntityDependency.handle_finding_policy,
                    EntityDependency.handle_vulnerabilities_acceptance,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.reset_expired_accepted_findings,
                    EntityDependency.update_vulnerabilities_treatment,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.verification_summary: dict(
                dependencies={
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_hold,
                    EntityDependency.request_vulnerabilities_verification,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.where: dict(
                dependencies={
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.reject_vulnerabilities_zero_risk,
                    EntityDependency.remove_vulnerability,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.update_vulnerability_commit,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
        },
    ),
    Entity.root: dict(
        args={
            EntityId.ids,
        },
        attrs={
            EntityAttr.last_status_update: dict(
                dependencies={
                    EntityDependency.activate_root,
                    EntityDependency.deactivate_root,
                }
            ),
        },
    ),
    Entity.vulnerability: dict(
        args={
            EntityId.ids,
        },
        attrs={
            EntityAttr.closing_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.efficacy: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.last_reattack_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.upload_file,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
            EntityAttr.last_reattack_requester: dict(
                dependencies={
                    EntityDependency.request_vulnerabilities_verification,
                }
            ),
            EntityAttr.last_requested_reattack_date: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_verification,
                }
            ),
            EntityAttr.reattack_cycles: dict(
                dependencies={
                    EntityDependency.deactivate_root,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_verification,
                }
            ),
            EntityAttr.report_date: dict(
                dependencies={
                    EntityDependency.confirm_vulnerabilities,
                    EntityDependency.upload_file,
                }
            ),
            EntityAttr.treatment_changes: dict(
                dependencies={
                    EntityDependency.handle_vulnerabilities_acceptance,
                    EntityDependency.handle_finding_policy,
                    EntityDependency.move_root,
                    EntityDependency.request_vulnerabilities_zero_risk,
                    EntityDependency.reset_expired_accepted_findings,
                    EntityDependency.update_vulnerabilities_treatment,
                    EntityDependency.verify_vulnerabilities_request,
                }
            ),
        },
    ),
}


def get_entities_to_update_by_dependency(
    dependency: EntityDependency, **args: list[str]
) -> dict[Entity, EntityToUpdate]:
    entities_to_update = {}
    for name, value in ENTITIES.items():
        attributes_to_update = set()
        for attr, info in cast(dict, value["attrs"]).items():
            if dependency in info["dependencies"]:
                attributes_to_update.add(attr)

        if attributes_to_update:
            entity_args = cast(set, value["args"])
            entity_ids = {
                base_arg: args[f"{name.value}_{base_arg.value}"]
                for base_arg in entity_args
            }
            entities_to_update[name] = EntityToUpdate(
                entity_ids=entity_ids,
                attributes_to_update=attributes_to_update,
            )

    return entities_to_update
