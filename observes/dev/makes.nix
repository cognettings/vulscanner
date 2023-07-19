{
  inputs,
  outputs,
  ...
}: let
  products = with inputs.observesIndex; {
    observesCodeEtl = etl.code;
    observesAsmDal = common.asm_dal;
    observesServiceDbMigration = service.db_migration;
    observesServiceDbSnapshot = service.db_snapshot;
    observesServiceSuccessIndicators = service.success_indicators;
    observesTapCsv = tap.csv;
    observesTapCheckly = tap.checkly;
    observesTapBugsnag = tap.bugsnag;
    observesTapDynamo = tap.dynamo;
    observesTapGitlab = tap.gitlab;
    observesTapGoogleSheets = tap.google_sheets;
    observesTapJson = tap.json;
    observesTapMandrill = tap.mandrill;
    observesTapMixpanel = tap.mixpanel_2;
    observesTapZohoCrm = tap.zoho_crm;
    observesTargetRedshift = target.redshift_2;
    observesTargetS3 = target.s3;
    observesEtlDynamoConf = etl.dynamo;
    observesEtlGoogleSheets = etl.google_sheets;
    observesUtilsLogger2 = common.utils_logger_2;
  };
  dev_envs =
    builtins.mapAttrs (
      _: v: {
        source = [outputs."${v.env.dev}"];
      }
    )
    products;
in {
  dev =
    dev_envs
    // {
      observesPaginator = {
        source = [
          outputs."/observes/common/paginator/env/development"
        ];
      };
      observesPostgresClient = {
        source = [
          outputs."/observes/common/postgres-client/env/development"
        ];
      };
      observesPurity = {
        source = [
          outputs."/observes/common/purity/env/development"
        ];
      };
      observesSingerIO = {
        source = [
          outputs."/observes/common/singer-io/env/development"
        ];
      };
      observesCommonUtilsLogger = {
        source = [
          outputs."${inputs.observesIndex.common.utils_logger.new_env.dev}"
        ];
      };
    };
}
