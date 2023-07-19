let
  commonPath = "/observes/common";
  pipelinePath = "/observes/pipeline";
  servicePath = "/observes/service";
  singerPath = "/observes/singer";
  etlsPath = "/observes/etl";
  underscore_pkg = root: builtins.replaceStrings ["-"] ["_"] (baseNameOf root);
  standard_1 = root: {
    root = "${root}/src";
    env = {
      runtime = "${root}/env/runtime";
      dev = "${root}/env/development";
    };
    bin = "${root}/bin";
    src = "${root}/src/${underscore_pkg root}";
    tests = "${root}/src/tests";
    lint = "${root}/lint";
    test = "${root}/test";
  };
  standard_2 = root: {
    inherit root;
    src = "${root}/${underscore_pkg root}";
    check = {
      arch = "${root}/check/arch";
      tests = "${root}/check/tests";
      types = "${root}/check/types";
    };
    bin = "${root}/bin";
    env = {
      runtime = "${root}/env/runtime";
      dev = "${root}/env/dev";
    };
  };
  standard_3 = let
    no_arch_job = base:
      base
      // {
        check = builtins.removeAttrs base.check ["arch"];
      };
  in
    x: no_arch_job (standard_2 x);
  standard_4 = let
    no_runtime = base:
      base
      // {
        env = builtins.removeAttrs base.env ["runtime"];
      };
  in
    x: no_runtime (standard_3 x);
  standard_3_no_bin = x: builtins.removeAttrs (standard_3 x) ["bin"];
  override_attrs = old: override: old // override old;
in {
  inherit commonPath pipelinePath servicePath singerPath etlsPath;
  service = {
    db_migration =
      (standard_1 "${servicePath}/db-migration")
      // {
        root = "${servicePath}/db-migration/src";
      };
    db_snapshot = standard_3 "${servicePath}/db-snapshot";
    success_indicators = standard_3 "${servicePath}/success-indicators";
  };
  etl = {
    dynamo = override_attrs (standard_3 "${etlsPath}/dynamo") (
      old: {
        src = "${old.root}/dynamo_etl_conf";
      }
    );
    code =
      (standard_3 "${etlsPath}/code")
      // {
        src = "${etlsPath}/code/code_etl";
      };
    google_sheets = standard_3 "${etlsPath}/google-sheets";
  };
  common = {
    asm_dal = standard_3 "${commonPath}/asm-dal";
    paginator = "${commonPath}/paginator";
    postgresClient = "${commonPath}/postgres-client/src";
    purity = "${commonPath}/purity";
    singer_io =
      standard_1 "${commonPath}/singer-io"
      // {
        env2.dev = "${commonPath}/singer-io/env2/dev";
      };
    utils_logger =
      standard_1 "${commonPath}/utils-logger"
      // {
        new_env.dev = "${commonPath}/utils-logger/new-env/dev";
      };
    utils_logger_2 = standard_3_no_bin "${commonPath}/utils-logger-2";
  };
  tap = {
    announcekit = standard_1 "${singerPath}/tap-announcekit";
    bugsnag = standard_3 "${singerPath}/tap-bugsnag";
    checkly = standard_3 "${singerPath}/tap-checkly";
    csv = standard_4 "${singerPath}/tap-csv";
    delighted = standard_1 "${singerPath}/tap-delighted";
    dynamo = standard_3 "${singerPath}/tap-dynamo";
    formstack = standard_1 "${singerPath}/tap-formstack";
    git = standard_1 "${singerPath}/tap-git";
    gitlab = standard_2 "${singerPath}/tap-gitlab";
    google_sheets = let
      root = "${singerPath}/tap-google-sheets";
    in {
      inherit root;
      env = {
        runtime = "${root}/env/runtime";
        dev = "${root}/env/dev";
      };
    };
    json = standard_3 "${singerPath}/tap-json";
    mailchimp = standard_1 "${singerPath}/tap-mailchimp";
    mandrill = standard_3 "${singerPath}/tap-mandrill";
    matomo = standard_1 "${singerPath}/tap-matomo";
    mixpanel = standard_1 "${singerPath}/tap-mixpanel";
    mixpanel_2 =
      standard_3 "${singerPath}/tap-mixpanel"
      // {
        env = {
          runtime = "${singerPath}/tap-mixpanel/env/runtime_2";
          dev = "${singerPath}/tap-mixpanel/env/dev";
        };
      };
    timedoctor = standard_1 "${singerPath}/tap-timedoctor";
    zoho_analytics = standard_1 "${singerPath}/tap-zoho-analytics";
    zoho_crm = standard_4 "${singerPath}/tap-zoho-crm";
  };
  target = {
    s3 = standard_3 "${singerPath}/target-s3";
    redshift = standard_2 "${singerPath}/target-redshift";
    redshift_2 =
      standard_3 "${singerPath}/target-redshift-2"
      // {
        src = "${singerPath}/target-redshift-2/target_redshift";
      };
  };
}
