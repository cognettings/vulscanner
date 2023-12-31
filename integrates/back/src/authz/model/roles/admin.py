from authz.model.types import (
    RoleLevel,
)

ADMIN_ROLE: dict[str, RoleLevel] = dict(
    group_level=RoleLevel(
        actions={
            "api_mutations_activate_root_mutate",
            "api_mutations_add_event_consult_mutate",
            "api_mutations_add_event_mutate",
            "api_mutations_add_files_mutate",
            "api_mutations_add_files_to_db_mutate",
            "api_mutations_add_finding_mutate",
            "api_mutations_add_finding_consult_mutate",
            "api_mutations_add_git_root_mutate",
            "api_mutations_add_group_consult_mutate",
            "api_mutations_add_group_tags_mutate",
            "api_mutations_add_ip_root_mutate",
            "api_mutations_add_url_root_mutate",
            "api_mutations_approve_evidence_mutate",
            "api_mutations_confirm_vulnerabilities_mutate",
            "api_mutations_confirm_vulnerabilities_zero_risk_mutate",
            "api_mutations_deactivate_root_mutate",
            "api_mutations_move_root_mutate",
            "api_mutations_download_event_file_mutate",
            "api_mutations_download_file_mutate",
            "api_mutations_download_vulnerability_file_mutate",
            "api_mutations_update_group_access_info_mutate",
            "api_mutations_update_group_disambiguation_mutate",
            "api_mutations_update_group_info_mutate",
            "api_mutations_update_group_managed_mutate",
            "api_mutations_update_group_mutate",
            "api_mutations_update_group_policies_mutate",
            "api_mutations_update_group_stakeholder_mutate",
            "api_mutations_grant_stakeholder_access_mutate",
            "api_mutations_reject_event_solution_mutate",
            "api_mutations_reject_vulnerabilities_mutate",
            "api_mutations_reject_vulnerabilities_zero_risk_mutate",
            "api_mutations_remove_finding_mutate",
            "api_mutations_remove_event_evidence_mutate",
            "api_mutations_remove_files_mutate",
            "api_mutations_remove_finding_evidence_mutate",
            "api_mutations_remove_group_mutate",
            "api_mutations_remove_group_tag_mutate",
            "api_mutations_remove_stakeholder_access_mutate",
            "api_mutations_remove_vulnerability_mutate",
            "api_mutations_request_event_verification_mutate",
            "api_mutations_request_vulnerabilities_verification_mutate",
            "api_mutations_request_vulnerabilities_zero_risk_mutate",
            "api_mutations_request_vulnerabilities_hold_mutate",
            "api_mutations_send_vulnerability_notification_mutate",
            "api_mutations_sign_post_url_mutate",
            "api_mutations_solve_event_mutate",
            "api_mutations_sync_git_root_mutate",
            "api_mutations_unsubscribe_from_group_mutate",
            "api_mutations_update_event_mutate",
            "api_mutations_update_event_evidence_mutate",
            "api_mutations_update_evidence_description_mutate",
            "api_mutations_update_evidence_mutate",
            "api_mutations_update_finding_description_mutate",
            "api_mutations_update_forces_access_token_mutate",
            "api_mutations_update_git_environments_mutate",
            "api_mutations_update_git_root_mutate",
            "api_mutations_update_ip_root_mutate",
            "api_mutations_update_root_cloning_status_mutate",
            "api_mutations_update_root_state_mutate",
            "api_mutations_update_toe_lines_sorts_mutate",
            "api_mutations_update_severity_mutate",
            "api_mutations_update_url_root_mutate",
            "api_mutations_update_vulnerability_description_mutate",
            "api_mutations_update_vulnerabilities_severity_mutate",
            "api_mutations_upload_file_mutate",
            "api_mutations_validate_git_access_mutate",
            "api_mutations_verify_vulnerabilities_request_mutate",
            "api_resolvers_finding_consulting_resolve",
            "api_resolvers_finding_drafts_connection_resolve",
            "api_resolvers_event_hacker_resolve",
            "api_resolvers_finding_hacker_resolve",
            "api_resolvers_finding_historic_state_resolve",
            "api_resolvers_finding_observations_resolve",
            "api_resolvers_finding_sorts_resolve",
            "api_resolvers_finding_zero_risk_resolve",
            "api_resolvers_finding_zero_risk_connection_resolve",
            "api_resolvers_git_environment_url_secrets_resolve",
            "api_resolvers_git_root_download_url_resolve",
            "api_resolvers_git_root_secrets_resolve",
            "api_resolvers_url_root_secrets_resolve",
            "api_resolvers_git_root_upload_url_resolve",
            "api_resolvers_group_analytics_resolve",
            "api_resolvers_group_billing_resolve",
            "api_resolvers_group_consulting_resolve",
            "api_resolvers_group_drafts_resolve",
            "api_resolvers_group_forces_executions_resolve",
            "api_resolvers_group_forces_executions_connection_resolve",
            "api_resolvers_group_forces_token_resolve",
            "api_resolvers_group_forces_exp_date_resolve",
            "api_resolvers_group_events_resolve",
            "api_resolvers_group_service_attributes_resolve",
            "api_resolvers_group_stakeholders_resolve",
            "api_resolvers_group_toe_inputs_resolve",
            "api_resolvers_group_toe_lines_resolve",
            "api_resolvers_group_toe_lines_connection_resolve",
            "api_resolvers_group_vulnerability_drafts_resolve",
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
            "api_resolvers_vulnerability_historic_verification_resolve",
            "api_resolvers_vulnerability_historic_zero_risk_resolve",
            "grant_group_level_role:architect",
            "grant_group_level_role:customer_manager",
            "grant_group_level_role:hacker",
            "grant_group_level_role:reattacker",
            "grant_group_level_role:resourcer",
            "grant_group_level_role:reviewer",
            "grant_group_level_role:user",
            "grant_group_level_role:user_manager",
            "grant_group_level_role:vulnerability_manager",
            "post_finding_observation",
            "update_git_root_filter",
            "request_group_upgrade",
            "see_group_services_info",
            "api_mutations_add_secret_mutate",
            "api_mutations_remove_secret_mutate",
            "api_mutations_add_git_environment_secret_mutate",
            "api_mutations_add_git_environment_mutate",
            "api_mutations_close_vulnerabilities_mutate",
            "api_mutations_remove_environment_url_mutate",
            "api_mutations_remove_environment_url_secret_mutate",
            "api_resolvers_query_environment_url_resolve",
            "api_resolvers_git_root_credentials_get_credentials_value",
            "api_mutations_add_toe_input_mutate",
            "api_mutations_add_toe_lines_mutate",
            "api_mutations_add_toe_port_mutate",
            "api_mutations_refresh_toe_lines_mutate",
            "api_mutations_submit_group_machine_execution_mutate",
            "api_mutations_submit_machine_job_mutate",
            "api_mutations_resubmit_vulnerabilities_mutate",
            "api_mutations_update_group_payment_id_mutate",
            "api_mutations_update_subscription_mutate",
            "api_mutations_update_toe_input_mutate",
            "api_mutations_update_toe_lines_attacked_lines_mutate",
            "api_mutations_update_toe_port_mutate",
            "api_resolvers_finding_machine_jobs_resolve",
            "api_resolvers_finding_rejected_vulnerabilities_resolve",
            "api_resolvers_finding_submitted_vulnerabilities_resolve",
            "api_resolvers_group_disambiguation_resolve",
            "api_resolvers_query_finding__get_draft",
            "api_resolvers_query_vulnerability__get_draft",
            "api_resolvers_toe_input_attacked_at_resolve",
            "api_resolvers_toe_input_attacked_by_resolve",
            "api_resolvers_toe_input_be_present_until_resolve",
            "api_resolvers_toe_input_first_attack_at_resolve",
            "api_resolvers_toe_input_seen_first_time_by_resolve",
            "api_resolvers_toe_lines_attacked_at_resolve",
            "api_resolvers_toe_lines_attacked_by_resolve",
            "api_resolvers_toe_lines_attacked_lines_resolve",
            "api_resolvers_toe_lines_be_present_until_resolve",
            "api_resolvers_toe_lines_comments_resolve",
            "api_resolvers_toe_lines_first_attack_at_resolve",
            "api_resolvers_toe_port_attacked_at_resolve",
            "api_resolvers_toe_port_attacked_by_resolve",
            "api_resolvers_toe_port_be_present_until_resolve",
            "api_resolvers_toe_port_first_attack_at_resolve",
            "api_resolvers_toe_port_seen_first_time_by_resolve",
            "api_resolvers_vulnerability_hacker_resolve",
            "see_draft_status",
            "see_internal_toe",
            "see_review_filter",
            "see_toe_lines_coverage",
            "see_toe_lines_days_to_attack",
            "see_vulnerability_source",
        },
        tags=set(),
    ),
    organization_level=RoleLevel(
        actions={
            "api_mutations_add_group_mutate",
            "api_mutations_update_organization_stakeholder_mutate",
            "api_mutations_grant_stakeholder_organization_access_mutate",
            "api_mutations_remove_stakeholder_organization_access_mutate",
            "api_mutations_update_organization_policies_mutate",
            "api_resolvers_organization_analytics_resolve",
            "api_resolvers_organization_billing_resolve",
            "api_resolvers_organization_stakeholders_resolve",
            "api_resolvers_organization_vulnerabilities_url_resolve",
            "api_resolvers_query_stakeholder__resolve_for_organization",
            "grant_organization_level_role:user",
            "grant_organization_level_role:user_manager",
            "api_mutations_add_credentials_mutate",
            "api_mutations_add_credit_card_payment_method_mutate",
            "api_mutations_add_other_payment_method_mutate",
            "api_mutations_download_billing_file_mutate",
            "api_mutations_remove_credentials_mutate",
            "api_mutations_remove_payment_method_mutate",
            "api_mutations_update_credentials_mutate",
            "api_mutations_update_credit_card_payment_method_mutate",
            "api_mutations_update_other_payment_method_mutate",
            "api_mutations_update_payment_method_mutate",
            "api_resolvers_billing_prices_resolve",
            "api_resolvers_query_billing_resolve",
            "grant_organization_level_role:customer_manager",
            "see_billing_service_type",
            "see_billing_subscription_type",
        },
        tags=set(),
    ),
    user_level=RoleLevel(
        actions={
            "api_mutations_submit_group_machine_execution_mutate",
            "api_mutations_add_group_mutate",
            "api_mutations_add_organization_mutate",
            "api_mutations_add_stakeholder_mutate",
            "api_mutations_update_stakeholder_phone_mutate",
            "api_mutations_verify_stakeholder_mutate",
            "api_resolvers_query_groups_resolve",
            "api_resolvers_query_list_user_groups_resolve",
            "api_resolvers_query_vulnerabilities_to_reattack_resolve",
            "grant_user_level_role:admin",
            "grant_user_level_role:hacker",
            "grant_user_level_role:user",
            "front_can_edit_credentials_secrets_in_bulk",
            "front_can_enable_meeting_mode",
            "front_can_retrieve_todo_drafts",
            "front_can_retrieve_todo_events",
            "front_can_retrieve_todo_locations_drafts",
            "front_can_retrieve_todo_reattacks",
            "api_resolvers_event_hacker_resolve",
            "api_resolvers_finding_hacker_resolve",
            "can_assign_vulnerabilities_to_fluidattacks_staff",
        },
        tags=set(),
    ),
)
