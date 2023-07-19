{
  gitlabCi,
  inputs,
  ...
}: let
  # rules
  gitlabBranchTrunk = gitlabCi.rules.branch "trunk";
  gitlabBranchNotTrunk = gitlabCi.rules.branchNot "trunk";
  gitlabTitleMatchingObserves = gitlabCi.rules.titleMatching "^(all|observes)";
  gitlabOnlyDev = changes: [
    gitlabBranchNotTrunk
    gitlabCi.rules.notMrs
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    (gitlabTitleMatchingObserves // {"changes" = changes;})
  ];
  gitlabOnlyProd = [
    gitlabBranchTrunk
    gitlabCi.rules.notSchedules
    gitlabCi.rules.notTriggers
    gitlabTitleMatchingObserves
  ];
  # confs
  gitlabDeployInfra = {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    resource_group = "$CI_JOB_NAME";
    rules = gitlabOnlyProd;
    stage = "deploy-infra";
    tags = ["observes-small"];
  };
  gitlabBuild = changes: {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev changes;
    stage = "build";
    tags = ["observes-small"];
  };
  gitlabLint = changes: {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev changes;
    stage = "lint-code";
    tags = ["observes-small"];
  };
  gitlabTestInfra = changes: {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev changes;
    stage = "test-infra";
    tags = ["observes-small"];
  };
  gitlabTestCode = changes: {
    image = "ghcr.io/fluidattacks/makes/arm64:latest";
    rules = gitlabOnlyDev changes;
    stage = "test-code";
    tags = ["observes-small"];
  };
  # new standard
  index = inputs.observesIndex;
  std_pkgs = with index; [
    common.asm_dal
    common.utils_logger_2
    etl.code
    etl.dynamo
    etl.google_sheets
    service.db_snapshot
    service.success_indicators
    tap.csv
    tap.checkly
    tap.dynamo
    tap.gitlab
    tap.json
    tap.mandrill
    tap.zoho_crm
    target.s3
    target.redshift_2
  ];
  _if_exists = attrs: key: function: default:
    if builtins.hasAttr key attrs
    then function attrs."${key}"
    else default;
  # change triggers
  to_root_glob = pkg_root: builtins.elemAt (builtins.match "/(.*)" "${pkg_root}/**/*") 0; # PkgRoot -> Trigger
  common_trigger = map to_root_glob [index.commonPath index.pipelinePath]; # [Trigger]
  per_package_subtriggers = pkg: let
    # Pkg -> [Trigger]
    get_or = attrs: key: default:
      if builtins.hasAttr key attrs
      then builtins.getAttr key attrs
      else default;
    the_map = {
      "${index.etl.google_sheets.root}" = [
        index.tap.google_sheets.root
        index.target.redshift_2.root
      ];
    };
    triggers = get_or the_map pkg.root [];
  in
    map to_root_glob triggers;
  # jobs
  gen_pkg_jobs = pkg: let
    root_glob = to_root_glob pkg.root; # Trigger
    all_pkg_triggers = [root_glob] ++ (per_package_subtriggers pkg) ++ common_trigger;
    _gen_job = gitlabExtraChanges: output: {
      inherit output;
      gitlabExtra = gitlabExtraChanges all_pkg_triggers;
    };
    _lint = v: [(_gen_job gitlabLint v)];
    _test = v: [(_gen_job gitlabTestCode v)];
    _build = v: [(_gen_job gitlabBuild v)];

    arch_check = _if_exists pkg.check "arch" _lint [];
    types_check = _if_exists pkg.check "types" _lint [];
    tests_check = _if_exists pkg.check "tests" _test [];
    run_check = _if_exists pkg.check "runtime" _test [];
    env_dev = _if_exists pkg.env "dev" _build [];
    bin_test = _if_exists pkg "bin" (
      v: [(_gen_job gitlabBuild "${v} --help")]
    ) [];
  in
    arch_check ++ types_check ++ tests_check ++ run_check ++ env_dev ++ bin_test;
  pkgs_jobs = builtins.concatLists (map gen_pkg_jobs std_pkgs);
in {
  pipelines = {
    observes = {
      gitlabPath = "/observes/gitlab-ci.yaml";
      jobs =
        pkgs_jobs
        ++ [
          {
            output = "/deployTerraform/observes";
            gitlabExtra = gitlabDeployInfra;
          }
          {
            output = "/lintPython/imports/observesArch";
            gitlabExtra = gitlabLint (["observes/common/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesCommonPaginator";
            gitlabExtra = gitlabLint (["observes/common/paginator/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesCommonSingerIo";
            gitlabExtra = gitlabLint (["observes/common/singer-io/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesCommonPostgresClient";
            gitlabExtra = gitlabLint (["observes/common/postgres-client/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapAnnounceKit";
            gitlabExtra = gitlabLint (["observes/singer/tap-announcekit/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapBugsnag";
            gitlabExtra = gitlabLint (["${index.tap.bugsnag.root}/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapDelighted";
            gitlabExtra = gitlabLint (["observes/singer/tap-delighted/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapFormstack";
            gitlabExtra = gitlabLint (["observes/singer/tap-formstack/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapMailchimp";
            gitlabExtra = gitlabLint (["observes/singer/tap-mailchimp/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapMatomo";
            gitlabExtra = gitlabLint (["observes/singer/tap-matomo/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapMixpanel";
            gitlabExtra = gitlabLint (["observes/singer/tap-mixpanel/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/imports/observesTapTimedoctor";
            gitlabExtra = gitlabLint (["observes/singer/tap-timedoctor/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesCommonPaginator";
            gitlabExtra = gitlabLint (["observes/common/paginator/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesCommonSingerIo";
            gitlabExtra = gitlabLint (["observes/common/singer-io/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesCommonSingerIoTests";
            gitlabExtra = gitlabLint (["observes/common/singer-io/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesCommonPostgresClient";
            gitlabExtra = gitlabLint (["observes/common/postgres-client/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesCommonPostgresClientTests";
            gitlabExtra = gitlabLint (["observes/common/postgres-client/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapAnnounceKit";
            gitlabExtra = gitlabLint (["observes/singer/tap-announcekit/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapAnnounceKitTests";
            gitlabExtra = gitlabLint (["observes/singer/tap-announcekit/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapBugsnag";
            gitlabExtra = gitlabLint (["observes/singer/tap-bugsnag/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapDelighted";
            gitlabExtra = gitlabLint (["observes/singer/tap-delighted/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapFormstack";
            gitlabExtra = gitlabLint (["observes/singer/tap-formstack/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapMailchimp";
            gitlabExtra = gitlabLint (["observes/singer/tap-mailchimp/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapMailchimpTests";
            gitlabExtra = gitlabLint (["observes/singer/tap-mailchimp/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapMatomo";
            gitlabExtra = gitlabLint (["observes/singer/tap-matomo/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapMixpanel";
            gitlabExtra = gitlabLint (["observes/singer/tap-mixpanel/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapMixpanelTests";
            gitlabExtra = gitlabLint (["observes/singer/tap-mixpanel/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTapTimedoctor";
            gitlabExtra = gitlabLint (["observes/singer/tap-timedoctor/**/*"] ++ common_trigger);
          }
          {
            output = "/lintPython/module/observesTargetRedshift";
            gitlabExtra = gitlabLint (["observes/singer/target-redsfhit/**/*"] ++ common_trigger);
          }
          {
            output = "/lintTerraform/observes";
            gitlabExtra = gitlabLint (["observes/infra/**/*"] ++ common_trigger);
          }
          {
            output = "/pipelineOnGitlab/observes";
            gitlabExtra = gitlabLint (["observes/pipeline/**/*" "observes/.gitlab-ci.yml"] ++ common_trigger);
          }
          {
            output = "/observes/singer/tap-announcekit/fx-test";
            gitlabExtra = gitlabTestCode (["observes/singer/tap-announcekit/**/*"] ++ common_trigger);
          }
          {
            output = "/observes/common/singer-io/test";
            gitlabExtra = gitlabTestCode (["observes/common/singer-io/**/*"] ++ common_trigger);
          }
          {
            output = "/observes/singer/tap-announcekit/test";
            gitlabExtra = gitlabTestCode (["observes/singer/tap-announcekit/**/*"] ++ common_trigger);
          }
          {
            output = "/observes/singer/tap-mailchimp/test";
            gitlabExtra = gitlabTestCode (["observes/singer/tap-mailchimp/**/*"] ++ common_trigger);
          }
          {
            output = "/observes/singer/tap-mixpanel/test";
            gitlabExtra = gitlabTestCode (["observes/singer/tap-mixpanel/**/*"] ++ common_trigger);
          }
          {
            output = "/testTerraform/observes";
            gitlabExtra = gitlabTestInfra (["observes/infra/**/*"] ++ common_trigger);
          }
        ];
    };
  };
}
