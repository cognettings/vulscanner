# Schedule expressions:
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
# schedule.meta.requiredBy format is DD-MM-YYYY
{
  common_ci_clean = {
    attempts = 1;
    awsRole = "prod_common";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/common/ci/clean"
    ];
    enable = true;
    environment = ["CACHIX_AUTH_TOKEN"];
    meta = {
      description = ''
        Clean CI resources:

        - Orphan workers
        - Orphan SSH Keys
      '';
      lastReview = "04-07-2023";
      maintainers = [
        "acuberos"
        "dsalazar"
        "jperez"
      ];
      requiredBy = ["CI to avoid extra costs by orphan resources."];
    };
    parallel = 1;
    scheduleExpression = "cron(0 10 * * ? *)";
    size = "common_small";
    tags = {
      "Name" = "common_ci_clean_keys";
      "management:area" = "cost";
      "management:product" = "common";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_abandoned_trial_notification = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.abandoned_trial_notification.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send email notifications
        to resume or start over trial registration.
      '';
      lastReview = "25-06-2023";
      maintainers = [
        "jhurtado"
        "faristizabal"
      ];
      requiredBy = [
        ''
          ARM in order to prevent losing users
          that start onboarding services for a free trial.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 */1 * * ? *)";
    size = "integrates_small";
    tags = {
      "Name" = "abandoned_trial_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 3600;
  };
  integrates_charts_documents = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/charts/documents"
      "prod"
      "20"
      "batch"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Generate charts documents by executing
        the analytics generators and upload them to S3.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "slizcano"
        "jperez"
      ];
      requiredBy = [
        "Analytics view in the ARM."
      ];
    };
    parallel = 20;
    scheduleExpression = "cron(0 1 ? * 2-6 *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_charts_documents";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 10800;
  };
  integrates_charts_snapshots = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/charts/snapshots"
      "prod"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Generate charts snapshots by executing
        the analytics generators using Selenium and upload them to S3.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "slizcano"
        "jperez"
      ];
      requiredBy = [
        "Analytics view in the ARM."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(45 3 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_charts_snapshots";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  common_clean_dev_ephemerals = {
    attempts = 3;
    awsRole = "prod_common";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/common/dev/clean/ephemerals"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Destroy ephemerals by destroying resources in dev namespace.
      '';
      lastReview = "11-07-2023";
      maintainers = [
        "dsalazar"
        "kcamargo"
      ];
      requiredBy = [
        "CI in order to free unused resources each day."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 0,5 * * ? *)";
    size = "common_small";
    tags = {
      "Name" = "common_clean_dev_environments";
      "management:area" = "cost";
      "management:product" = "common";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  common_clean_dev_branches = {
    attempts = 3;
    awsRole = "prod_common";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/common/dev/clean/branches"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "CI_PROJECT_ID"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Delete all repository branches except those with open merge request.
      '';
      lastReview = "11-07-2023";
      maintainers = [
        "dsalazar"
        "kcamargo"
      ];
      requiredBy = [
        "CI in order to free unused resources each day."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 7 * * ? *)";
    size = "common_small";
    tags = {
      "Name" = "common_clean_dev_branches";
      "management:area" = "cost";
      "management:product" = "common";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_woker = {
    attempts = 3;
    awsRole = "prod_common";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/deployTerraform/workerInfra"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Updates the deployment of the task worker, does the deployment
        with the latest commit of universe
      '';
      lastReview = "20-06-2023";
      maintainers = [
        "drestrepo"
        "acuberos"
      ];
      requiredBy = [
        "Integrates tasks worker"
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11-23/2 * * ? *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_update_woker";
      "management:area" = "cost";
      "management:product" = "skims";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  common_update_hearbeats = {
    attempts = 3;
    awsRole = "prod_common";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/common/status/schedules"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Updates the deployment of the better stack hearbeats monitor
      '';
      lastReview = "27-06-2023";
      maintainers = [
        "drestrepo"
        "dacevedo"
      ];
      requiredBy = [
        "Better Stack"
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 */2 * * ? *)";
    size = "common_small";
    tags = {
      "Name" = "common_update_hearbeats";
      "management:area" = "cost";
      "management:product" = "common";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_clone_groups_roots = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.clone_groups_roots.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    statusPage = true;
    resourceName = "Active roots cloning";
    meta = {
      description = ''
        Clone all the roots in active groups
        that have credentials associated and upload them to S3.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "drestrepo"
        "acuberos"
      ];
      requiredBy = [
        "Security testers for analyzing up-to-date repositories."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 10-23/2 ? * 2-6 *)";
    size = "clone";
    tags = {
      "Name" = "integrates_clone_groups_roots";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_clone_roots_that_have_not_cloned = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.clone_roots_that_have_not_cloned.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    statusPage = true;
    resourceName = "Full roots cloning";
    meta = {
      description = ''
        Clone all the roots in active groups that have credentials associated
        that not has been cloned in the las three days and upload them to S3.
      '';
      lastReview = "10-07-2023";
      maintainers = [
        "drestrepo"
        "acuberos"
      ];
      requiredBy = [
        "Security testers for analyzing up-to-date repositories."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11 ? * 3-6 *)";
    size = "clone";
    tags = {
      "Name" = "integrates_clone_roots_that_have_not_cloned";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_consulting_digest_notification = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.consulting_digest_notification.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send emails to users with comments digest.
      '';
      lastReview = "25-06-2023";
      maintainers = [
        "jhurtado"
        "jmesa"
      ];
      requiredBy = [
        ''
          ARM sending only one mail with all comments summary
          and avoid email flooding to users.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11,19 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_consulting_digest_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_delete_obsolete_groups = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_obsolete_groups.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Remove groups without users,
        findings nor Fluid Attacks services enabled.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "jmesa"
        "acaguirre"
      ];
      requiredBy = [
        "ARM cleaning unwanted or obsolete data."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 2 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_delete_obsolete_groups";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_delete_obsolete_orgs = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.delete_obsolete_orgs.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Remove organizations without groups after 60 days.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "jmesa"
        "acaguirre"
      ];
      requiredBy = [
        "ARM cleaning unwanted or obsolete data."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 9 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_delete_obsolete_orgs";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_event_digest_notification = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.event_digest_notification.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send emails to users with events digest.
      '';
      lastReview = "25-06-2023";
      maintainers = [
        "jhurtado"
        "jmesa"
      ];
      requiredBy = [
        ''
          ARM sending a consolidated events summary
          and avoid email flooding to users.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_event_digest_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_event_report = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.event_report.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send emails to users with events summary.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "jhurtado"
        "jvillegas"
      ];
      requiredBy = [
        ''
          ARM sending a consolidated events summary
          and avoid email flooding to users.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 14 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_event_report";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_expire_free_trial = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.expire_free_trial.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Validate expiration date for trial groups updating their state
        and clean data for already expired groups.
      '';
      lastReview = "13-07-2023";
      maintainers = [
        "dacevedo"
        "jmesa"
      ];
      requiredBy = [
        "ARM autoenrollment flow as the free trial expiration
        needs to be automatic."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(59 23 ? * MON-FRI *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_expire_free_trial";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 3600;
  };
  integrates_groups_languages_distribution = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.groups_languages_distribution.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "INTEGRATES_API_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Download all active group repositories
        and executes tokei over them.
        Save the results at the root level (individual)
        and at the group level (overall).
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "acuberos"
        "jmesa"
      ];
      requiredBy = [
        "ARM collecting information on repositories language distribution."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 10 ? * 2,5 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_groups_languages_distribution";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 21600;
  };
  integrates_machine_queue_all = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.machine_queue_all.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Queue machine executions for all active groups.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "drestrepo"
        "acuberos"
      ];
      requiredBy = [
        "Machine as it needs to run periodically over every group."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 13 ? * 7 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_machine_queue_all";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_machine_queue_re_attacks = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.machine_queue_re_attacks.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Queue pending reattacks
        on open vulnerabilities with a requested verification.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "drestrepo"
        "acuberos"
      ];
      requiredBy = [
        "Machine in order to ensure that reattacks are verified."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 12,21 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_machine_queue_re_attacks";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_machine_vulnerability_notification = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.machine_vulnerability_notification.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send machine vulnerability notification four times a day.
      '';
      lastReview = "01-07-2023";
      maintainers = [
        "jhurtado"
        "faristizabal"
      ];
      requiredBy = [
        ''
          ARM to report vulnerabilities from machine.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 0,6,12,18 * * ? *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_machine_vulnerability_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_migration_for_removing_sorts_attr = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/db/migration"
      "prod"
      "0414_rm_sorts_normalized_attr.py"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Migration for removing all instances of the
        sorts_risk_level_normalized attr from the db
      '';
      lastReview = "14-07-2023";
      maintainers = [
        "rrodriguez"
        "dacevedo"
      ];
      requiredBy = [
        ''
          Integrates because the attribute that isn't needed
          anymore should be removed
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * 6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_migration_for_removing_sorts_attr";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_migration_for_updating_indicators = {
    attempts = 2;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/db/migration"
      "prod"
      "0406_update_findings_indicators.py"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update all findings indicators in db.
      '';
      lastReview = "07-07-2023";
      maintainers = [
        "jdiaz"
        "dacevedo"
      ];
      requiredBy = [
        ''
          Inconsistent information in ARM findings view
          requires an update of the indicators.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0,30 10-11,22-23 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_migration_for_updating_indicators";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_missing_environment_alert = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.missing_environment_alert.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send emails when a group does not have registered environments URLs.
      '';
      lastReview = "26-06-2023";
      maintainers = [
        "jhurtado"
        "jvillegas"
      ];
      requiredBy = [
        "ARM to ensure the environments data is given."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_missing_environment_alert";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_newsletter = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.newsletter.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send monthly newsletter email.
      '';
      lastReview = "04-07-2023";
      maintainers = [
        "jhurtado"
        "faristizabal"
      ];
      requiredBy = [
        ''
          ARM sending newsletter to effectively communicate feature changes.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(30 21 4 * ? *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_newsletter";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_numerator_report_digest = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.numerator_report_digest.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Automates the enumerator report and send an email notification with it.
      '';
      lastReview = "26-06-2023";
      maintainers = [
        "jhurtado"
        "jvillegas"
      ];
      requiredBy = [
        "Hackers as they need to fill out this report daily."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 10 ? * 2-6 *)";
    size = "integrates_large";
    tags = {
      "Name" = "integrates_numerator_report_digest";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 129600;
  };
  integrates_organization_vulnerabilities = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.organization_vulnerabilities.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Build an artifact with all vulnerabilities
        from an organization and store it in S3.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "slizcano"
        "jmesa"
      ];
      requiredBy = [
        "ARM to ease downloading all data from a group or an organization."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(30 1,5,9,13,17,21 ? * 2-6 *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_organization_vulnerabilities";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 43200;
  };
  integrates_refresh_toe_lines = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.refresh_toe_lines.main"
    ];
    enable = false;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Refresh the ToE lines in all active groups.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "acaguirre"
        "drestrepo"
      ];
      requiredBy = [
        "ARM to update surface view and related data."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 20 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_refresh_toe_lines";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_reminder_notification = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.reminder_notification.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send an email to users inactive during three weeks.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "jhurtado"
        "jvillegas"
      ];
      requiredBy = [
        "ARM as some users stop using the platform."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 19 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_reminder_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_remove_inactive_stakeholders = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.remove_inactive_stakeholders.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Remove inactive stakeholders
        according to the related organization policy.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "jmesa"
        "dacevedo"
      ];
      requiredBy = [
        ''
          ARM to ensure the removal for users
          that have left the company
          or no longer have interest in the platform.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 1 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_remove_inactive_stakeholders";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_report_squad_usage = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.report_squad_usage.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Report Squad subscription usage to Stripe.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "dacevedo"
        "kcamargo"
      ];
      requiredBy = [
        ''
          ARM billing costumer module as part of the autoenrollment flow.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 18,00 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_report_squad_usage";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_requeue_actions = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.requeue_actions.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send pending actions/jobs to batch when unsuccessful and update
        their state in DynamoDB table fi_async_processing.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "drestrepo"
        "acuberos"
      ];
      requiredBy = [
        ''
          Batch as actions/jobs could fail and they will be resend a certain
          number of attempts.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(15 * ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_requeue_actions";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_reset_expired_accepted_findings = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.reset_expired_accepted_findings.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update treatment for vulnerabilities where acceptance
        date has expired. This applies for both accepted and
        accepted undefined treatment statuses.
      '';
      lastReview = "20-06-2023";
      maintainers = [
        "jmesa"
        "dacevedo"
      ];
      requiredBy = [
        ''
          ARM in order to comply with treatment acceptance expiration
          dates and fulfill the accepted treatment flow.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 0 ? * * *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_reset_expired_accepted_findings";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_review_machine_executions = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.review_machine_executions.main"
    ];
    enable = false;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Requeue machine executions that are suspected to be
        paused due to an unknown reason.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "drestrepo"
        "acuberos"
      ];
      requiredBy = [
        ''
          Machine in order to run on all groups as expected.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(30 * ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_review_machine_executions";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_send_deprecation_notice = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.send_deprecation_notice.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send a mail to all users notifying a deprecated field,
        mutation, etc, will be soon removed from the ARM API.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "jchaves"
        "dacevedo"
      ];
      requiredBy = [
        ''
          ARM users as API deprecations could go unnoticed
          by the customers, breaking their integrations.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 12 12 * ? *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_send_deprecation_notice";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_reviewer_progress_report = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.reviewer_progress_report.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Automates the reviewer report and send an email notification with it.
      '';
      lastReview = "13-07-2023";
      maintainers = [
        "acaguirre"
        "jvillegas"
      ];
      requiredBy = [
        "Reviewers as they need to fill out this report daily."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 6 ? * 2-6 *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_reviewer_progress_report";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 21600;
  };
  integrates_send_trial_engagement_notification = {
    attempts = 1;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.send_trial_engagement_notification.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send engagement notification emails to free trial users
        making them aware of the platform features and communication
        channels.
      '';
      lastReview = "25-06-2023";
      maintainers = [
        "jhurtado"
        "faristizabal"
      ];
      requiredBy = [
        ''
          ARM as part of the free trial flow leveraging on the free
          trial to boost user engagement.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 15 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_send_trial_engagement_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 3600;
  };
  integrates_treatment_alert_notification = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.treatment_alert_notification.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Send an alert email with a list of the
        accepted vulnerabilities in a given group
        whose acceptance date is close to expire.
      '';
      lastReview = "26-06-2023";
      maintainers = [
        "jhurtado"
        "jvillegas"
      ];
      requiredBy = [
        ''
          ARM sending only one mail with all related
          accepted treatment summary
          and avoid email flooding to users.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * 2-6 *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_treatment_alert_notification";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_compliance = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_compliance.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update all organizations compliance indicators.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "acaguirre"
        "jmesa"
      ];
      requiredBy = [
        ''
          ARM in order to update info that will be displayed
          in the organization compliance view.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_update_compliance";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_group_toe_sorts = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_group_toe_sorts.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update all sorts attributes for all active groups'
        toe lines retrieving sorts results from S3.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "rrodriguez"
        "dmurcia"
      ];
      requiredBy = [
        ''
          Sorts as updating this results using the ARM API
          is too slow.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 23 ? * 7 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_update_group_toe_sorts";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_group_toe_priority_factors = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_group_toe_priority_factors.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Calculate and update priority factors for all
        active groups' toe lines
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "rrodriguez"
        "dmurcia"
      ];
      requiredBy = [
        ''
          Sorts as updating this results using the ARM API
          is too slow.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 23 ? * 2-5 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_update_group_toe_priority_factors";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_group_toe_vulns = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_group_toe_vulns.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update the has_vulnerabilities attribute in the
        ToE surface
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "acaguirre"
        "jchaves"
      ];
      requiredBy = [
        ''
          ARM to display updated info in the surface view
          and related flows.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 10 ? * * *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_update_group_toe_vulns";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_indicators = {
    attempts = 2;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_indicators.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update all active groups unreliable indicators in db.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "slizcano"
        "jmesa"
      ];
      requiredBy = [
        ''
          ARM analytics as these preprocessed data is used
          is generating its charts.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 9,18 ? * 2-6 *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_update_indicators";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_organization_overview = {
    attempts = 2;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_organization_overview.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "INTEGRATES_API_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update organizations overview metrics in the
        unreliable indicators in db.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "slizcano"
        "jmesa"
      ];
      requiredBy = [
        ''
          ARM to display the organization overview metrics.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(30 20 ? * 6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_update_organization_overview";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 43200;
  };
  integrates_update_organization_repositories = {
    attempts = 2;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_organization_repositories.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update integration repositories data for all organizations.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "slizcano"
        "jmesa"
      ];
      requiredBy = [
        ''
          ARM to enable Azure DevOps integrations and to let the
          customers identify which repositories are not included in
          Fluid Attacks services.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(45 23 * * ? *)";
    size = "integrates_medium";
    tags = {
      "Name" = "integrates_update_organization_repositories";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  integrates_update_portfolios = {
    attempts = 3;
    awsRole = "prod_integrates";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/integrates/utils/scheduler"
      "prod"
      "schedulers.update_portfolios.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Update all portfolios unreliable indicators in db.
      '';
      lastReview = "05-07-2023";
      maintainers = [
        "slizcano"
        "jmesa"
      ];
      requiredBy = [
        ''
          ARM analytics as these preprocessed data is used
          is generating its charts.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 7,14 ? * 2-6 *)";
    size = "integrates_small";
    tags = {
      "Name" = "integrates_update_portfolios";
      "management:area" = "cost";
      "management:product" = "integrates";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  observes_etl_code_compute_bills = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/code/compute-bills"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Calculates Squad plan billed authors for groups.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "kcamargo"
      ];
      requiredBy = [
        "Integrates to show authors consumption"
        "Integrates to bill clients"
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 2,17 * * ? *)";
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_code_compute_bills";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 2 * 3600;
  };
  observes_etl_code_upload = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/code/upload/all-on-aws"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Triggers code ETL jobs for each group.
        The ETL fetch commits data from clients repositories.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "kcamargo"
      ];
      requiredBy = [
        "observes_etl_code_compute_bills"
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11 ? * 2-6 *)"; # workdays at 6am UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_code_upload";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 2 * 3600;
  };
  observes_etl_announcekit = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/announcekit"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from Announcekit
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          integrates announces.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * 2-6 *)"; # workdays at 12pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_announcekit";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 1 * 3600;
  };
  observes_etl_bugsnag = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/bugsnag"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from bugsnag
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          products errors.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * 2-6 *)"; # workdays at 12pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_bugsnag";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 4 * 3600;
  };
  observes_etl_checkly = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/checkly"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from Checkly
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          web stability to sites like
          integrates and the airs.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * 2-6 *)"; # workdays at 12pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_checkly";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 1 * 3600;
  };
  observes_etl_delighted = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/delighted"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from delighted
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          products errors.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * 2-6 *)"; # workdays at 12pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_delighted";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 1 * 3600;
  };
  observes_etl_dynamo = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/dynamo/jobs/run"
      "PHASE_1"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Triggers the mirror job, that
        mirrors data from dynamo DB
        into Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to perform
          data analitics.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 3 ? * 2-6 *)"; # (workdays-1) at 10pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_dynamo";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 1 * 3600;
  };
  observes_etl_dynamo_schema = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/dynamo/jobs/run"
      "DETERMINE_SCHEMA"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Triggers the job that
        determines the dynamo
        DB schema for Redshift.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        "observes_etl_dynamo"
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 3 ? * 7 *)"; # every FRI at 10pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_dynamo_schema";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 1 * 3600;
  };
  observes_etl_formstack = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/formstack"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from formstack
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          filled forms.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 16,23 ? * 1-6 *)";
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_formstack";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 6 * 3600;
  };
  observes_etl_gitlab_ephemeral = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/gitlab/universe/ephemeral"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from GitLab
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          product and development performance.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 17 ? * 2-6 *)"; # workdays at 12pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_gitlab_ephemeral";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 3 * 3600;
  };
  observes_etl_gitlab = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/gitlab/universe"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from GitLab
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          product and development performance.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11-23/4 ? * 2-6 *)"; # workdays at 6am-10am-2pm-6pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_gitlab_universe";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 4 * 3600;
  };
  observes_etl_mailchimp = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/mailchimp"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from Mailchimp
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          mail campaigns.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 20 ? * 2-6 *)"; # workdays at 3pm UTC-5
    size = "observes_medium";
    tags = {
      "Name" = "observes_etl_mailchimp";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 24 * 3600;
  };
  observes_etl_mandrill = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/mandrill"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from Mandrill
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          Mandrill (mailchimp add-on).
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 20 ? * 2-6 *)"; # workdays at 3pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_mandrill";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 2 * 3600;
  };
  observes_etl_matomo = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/matomo"
    ];
    enable = true;
    environment = [
      "CI_PROJECT_ID"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from Matomo
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics about
          web visits to sites like
          integrates and the airs.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 20 ? * 2-6 *)"; # workdays at 3pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_matomo";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 5 * 3600;
  };
  observes_etl_mixpanel = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/mixpanel"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from Mixpanel
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        "Business to track ARM events"
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 20 ? * 2-6 *)"; # workdays at 3pm UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_mixpanel";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 24 * 3600;
  };
  observes_etl_timedoctor = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/timedoctor"
    ];
    enable = true;
    environment = [
      "CI_PROJECT_ID"
    ];
    meta = {
      description = ''
        Extract entire Timedoctor
        history from s3
        and update redshift
        for later analytics usage.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics
          about employee working time
          and performance.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 9 ? * 2-6 *)";
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_timedoctor";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 24 * 3600;
  };
  observes_etl_timedoctor_backup = {
    attempts = 4;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/timedoctor/backup"
    ];
    enable = true;
    environment = [
      "CI_PROJECT_ID"
    ];
    meta = {
      description = ''
        Extract Timedoctor history
        from the last month
        and add it to S3.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          observes_etl_timedoctor
          as it uses the provided s3 history
          for populating Redshift.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 4 1 * ? *)";
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_timedoctor_backup";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 10 * 3600;
  };
  observes_etl_zoho_crm_fluid = {
    attempts = 2;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/zoho-crm/fluid"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Extract data from Zoho CRM
        to feed Redshift
        for later analytics processing.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          Business to track metrics
          about opportunities, contracts
          sales, etc.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 12 ? * 2-6 *)"; # workdays at 7am UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_zoho_crm_fluid";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 24 * 3600;
  };
  observes_etl_zoho_crm_fluid_prepare = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/etl/zoho-crm/fluid/prepare"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Create a request on Zoho CRM
        to export data that will later
        be user.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          observes_etl_zoho_crm_fluid
          as it uses the exported data
          once it becomes available.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 10 ? * 2-6 *)"; # workdays at 5am UTC-5
    size = "observes_small";
    tags = {
      "Name" = "observes_etl_zoho_crm_fluid_prepare";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 1 * 3600;
  };
  observes_service_snapshot = {
    attempts = 1;
    awsRole = "prod_observes";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/observes/service/db-snapshot/bin"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
    ];
    meta = {
      description = ''
        Create a manual snapshot of the redshift cluster.
        Manual snapshot, in contrast to automatic snapshots,
        have longer or even indefinite retention period.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "dmurcia"
        "rrodriguez"
      ];
      requiredBy = [
        ''
          business backups policy
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 0 L * ? *)"; # every last day of a month
    size = "observes_small";
    tags = {
      "Name" = "observes_service_snapshot";
      "management:area" = "cost";
      "management:product" = "observes";
      "management:type" = "product";
    };
    timeout = 1 * 3600;
  };
  skims_benchmark_owasp = {
    attempts = 3;
    awsRole = "prod_skims";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/skims/benchmark/owasp/upload"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Skims is executed with the test data provided by the owasp
        benchmark, then the results of the execution are
        compared with the results expected by the owasp benchmark.
      '';
      lastReview = "03-07-2023";
      maintainers = [
        "acuberos"
        "drestrepo"
      ];
      requiredBy = [
        "OWASP Foundation scanners list."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 11-23/2 * * ? *)";
    size = "skims_small";
    tags = {
      "Name" = "skims_benchmark_owasp";
      "management:area" = "cost";
      "management:product" = "skims";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  skims_update_sca_table = {
    attempts = 3;
    awsRole = "prod_skims";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/skims/sca/scheduler"
      "schedulers.update_sca_table.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Check sca vulnerabilities
        and update the vulnerability table in dynamo.
      '';
      lastReview = "03-07-2023";
      maintainers = [
        "acuberos"
        "drestrepo"
      ];
      requiredBy = [
        "Machine executions that query about sca vulnerabilities."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 10 * * ? *)";
    size = "skims_small";
    tags = {
      "Name" = "skims_update_sca_table";
      "management:area" = "cost";
      "management:product" = "skims";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  skims_clean_sca_table = {
    attempts = 3;
    awsRole = "prod_skims";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/skims/sca/scheduler"
      "schedulers.clean_sca_table.main"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "UNIVERSE_API_TOKEN"
    ];
    meta = {
      description = ''
        Check sca vulnerabilities, compare them with dynamo adviosires,
        remove from dynamo and s3 advisories that are no longer in the sources.
        remove manually sourced advisories that have the same metadata as
        their external source reference.
      '';
      lastReview = "04-07-2023";
      maintainers = [
        "acuberos"
        "jromero"
      ];
      requiredBy = [
        "Machine executions that query about sca vulnerabilities."
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 15 ? * 7 *)";
    size = "skims_small";
    tags = {
      "Name" = "skims_clean_sca_table";
      "management:area" = "cost";
      "management:product" = "skims";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  sorts_association_execute = {
    attempts = 3;
    awsRole = "prod_sorts";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/association-execute"
      "15"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "SORTS_TOKEN_FLUIDATTACKS"
    ];
    meta = {
      description = ''
        Compute and update the file's top 5
        most probable vuln types in the ARM.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "rrodriguez"
        "dmurcia"
      ];
      requiredBy = [
        ''
          Sorts,
          as the product requires the data
          to be shown in the ARM interface.
        ''
      ];
    };
    parallel = 15;
    scheduleExpression = "cron(0 23 ? * 7 *)";
    size = "sorts_small";
    tags = {
      "Name" = "sorts_association_execute";
      "management:area" = "cost";
      "management:product" = "sorts";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  sorts_association_rules = {
    attempts = 1;
    awsRole = "prod_sorts";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/association-rules/bin"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "SORTS_TOKEN_FLUIDATTACKS"
    ];
    meta = {
      description = ''
        Update the association rules based in the current available data.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "rrodriguez"
        "dmurcia"
      ];
      requiredBy = [
        ''
          sorts_association_execute,
          since these rules are used to compute
          the probability of each vulnerability type
          being present in a determined file.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 0 1 1-12/3 ? *)";
    size = "sorts_large";
    tags = {
      "Name" = "sorts_association_rules";
      "management:area" = "cost";
      "management:product" = "sorts";
      "management:type" = "product";
    };
    timeout = 86400;
  };
  sorts_execute = {
    attempts = 3;
    awsRole = "prod_sorts";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/execute"
      "20"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "SORTS_TOKEN_FLUIDATTACKS"
    ];
    meta = {
      description = ''
        Predict the priority for all present files in the ARM scope.
      '';
      lastReview = "30-06-2023";
      maintainers = [
        "rrodriguez"
        "dmurcia"
      ];
      requiredBy = [
        ''
          integrates_update_group_toe_priorities
          since these predictions are its input.
        ''
      ];
    };
    parallel = 20;
    scheduleExpression = "cron(0 23 ? * 6 *)";
    size = "sorts_small";
    tags = {
      "Name" = "sorts_execute";
      "management:area" = "cost";
      "management:product" = "sorts";
      "management:type" = "product";
    };
    timeout = 129600;
  };
  sorts_training_and_tune = {
    attempts = 1;
    awsRole = "prod_sorts";
    command = [
      "m"
      "gitlab:fluidattacks/universe@trunk"
      "/sorts/training-and-tune"
    ];
    enable = true;
    environment = [
      "CACHIX_AUTH_TOKEN"
      "SORTS_TOKEN_FLUIDATTACKS"
    ];
    meta = {
      description = "Full Machine Learning pipeline to train sorts.";
      lastReview = "04-07-2023";
      maintainers = [
        "rrodriguez"
        "dmurcia"
      ];
      requiredBy = [
        ''
          sorts_execute,
          since this model is used to calculate
          the priority for each file.
        ''
      ];
    };
    parallel = 1;
    scheduleExpression = "cron(0 5 ? * 6 *)";
    size = "sorts_small";
    tags = {
      "Name" = "sorts_training_and_tune";
      "management:area" = "cost";
      "management:product" = "sorts";
      "management:type" = "product";
    };
    timeout = 129600;
  };
}
