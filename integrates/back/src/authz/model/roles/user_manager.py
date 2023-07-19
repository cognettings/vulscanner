from authz.model.types import (
    RoleLevel,
)

USER_MANAGER_ROLE: dict[str, RoleLevel] = dict(
    group_level=RoleLevel(
        actions={
            "api_resolvers_group_forces_token_resolve",
            "api_resolvers_group_forces_exp_date_resolve",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_activate_root_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_move_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_files_to_db_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_update_group_access_info_mutate",
            "api_mutations_update_group_info_mutate",
            "api_mutations_update_group_policies_mutate",
            "api_mutations_update_group_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_handle_vulnerabilities_acceptation_mutate",
            "api_mutations_handle_vulnerabilities_acceptance_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_remove_vulnerability_tags_mutate",
            "api_mutations_request_event_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_mutate",
            "api_mutations_send_vulnerability_notification_mutate",
            "api_mutations_sign_post_url_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_ip_root_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_url_root_mutate",
            "api_mutations_update_vulnerability_treatment_mutate",
            "api_mutations_update_vulnerabilities_treatment_mutate",
            "api_mutations_send_assigned_notification_mutate",
            "api_mutations_sync_git_root_mutate",
            "api_mutations_validate_git_access_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_git_environment_url_secrets_resolve",
            "api_resolvers_git_root_secrets_resolve",
            "api_resolvers_url_root_secrets_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_billing_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_forces_executions_resolve",
            "api_resolvers_group_forces_executions_connection_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_group_toe_inputs_resolve",
            "api_resolvers_group_toe_lines_resolve",
            "api_resolvers_group_toe_lines_connection_resolve",
            "api_resolvers_query_toe_lines_report_resolve",
            "api_resolvers_group_toe_ports_resolve",
            "api_resolvers_query_event_resolve",
            "api_resolvers_query_events_resolve",
            "api_resolvers_query_finding_resolve",
            "api_resolvers_query_forces_execution_resolve",
            "api_resolvers_query_group_resolve",
            "api_resolvers_query_root_resolve",
            "api_resolvers_query_report__get_url_group_report",
            "api_resolvers_query_resources_resolve",
            "api_resolvers_query_stakeholder__resolve_for_group",
            "api_resolvers_query_unfulfilled_standard_report_url_resolve",
            "api_resolvers_query_vulnerability_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "grant_group_level_role:user",
            "grant_group_level_role:user_manager",
            "grant_group_level_role:vulnerability_manager",
            "grant_user_level_role:user",
            "update_git_root_filter",
            "valid_assigned",
            "request_group_upgrade",
            "api_mutations_add_secret_mutate",
            "api_mutations_remove_secret_mutate",
            "api_mutations_add_git_environment_secret_mutate",
            "api_mutations_add_git_environment_mutate",
            "api_mutations_remove_environment_url_mutate",
            "api_mutations_remove_environment_url_secret_mutate",
            "api_resolvers_query_environment_url_resolve",
        },
        tags=set(),
    ),
    organization_level=RoleLevel(
        actions={
            "api_mutations_add_credentials_mutate",
            "api_mutations_add_credit_card_payment_method_mutate",
            "api_mutations_add_group_mutate",
            "api_mutations_add_organization_finding_policy_mutate",
            "api_mutations_add_other_payment_method_mutate",
            "api_mutations_deactivate_finding_policy_mutate",
            "api_mutations_deactivate_organization_finding_policy_mutate",
            "api_mutations_download_billing_file_mutate",
            "api_mutations_handle_finding_policy_acceptance_mutate",
            "api_mutations_handle_finding_policy_acceptation_mutate",
            (
                "api_mutations_handle_organization_finding_policy_acceptation_"
                "mutate"
            ),
            (
                "api_mutations_handle_organization_finding_policy_acceptance_"
                "mutate"
            ),
            "api_mutations_update_organization_stakeholder_mutate",
            "api_mutations_grant_stakeholder_organization_access_mutate",
            "api_mutations_remove_credentials_mutate",
            "api_mutations_remove_stakeholder_organization_access_mutate",
            "api_mutations_submit_organization_finding_policy_mutate",
            "api_mutations_update_credentials_mutate",
            "api_mutations_update_credit_card_payment_method_mutate",
            "api_mutations_update_organization_policies_mutate",
            "api_mutations_update_other_payment_method_mutate",
            "api_mutations_update_payment_method_mutate",
            "api_resolvers_organization_analytics_resolve",
            "api_resolvers_organization_billing_resolve",
            "api_resolvers_organization_stakeholders_resolve",
            "api_resolvers_organization_vulnerabilities_url_resolve",
            "api_resolvers_query_stakeholder__resolve_for_organization",
            "grant_organization_level_role:user",
            "grant_organization_level_role:user_manager",
        },
        tags=set(),
    ),
)