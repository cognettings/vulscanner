{
  __system__,
  outputs,
  inputs,
  makeScript,
  projectPath,
  ...
}: let
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  env = pkg.outputs.packages."${__system__}".env.runtime;
  dynamoSchema = outputs."/computeOnAwsBatch/observesDynamoSchemaTestData";
  dynamoPhase1 = outputs."/computeOnAwsBatch/observesDynamoParallelPhase1";
  dynamoPhase3 = outputs."/computeOnAwsBatch/observesDynamoParallelPhase3";
  prepareLoading = outputs."/observes/etl/dynamo/jobs/prepare";
in
  makeScript {
    searchPaths = {
      bin = [
        env
      ];
      source = [
        outputs."/observes/common/db-creds"
      ];
    };
    replace = {
      __argDynamoPhase1__ = "${dynamoPhase1}/bin/${dynamoPhase1.name}";
      __argDynamoPhase3__ = "${dynamoPhase3}/bin/${dynamoPhase3.name}";
      __argPrepareLoading__ = "${prepareLoading}/bin/${prepareLoading.name}";
      __argDynamoSchema__ = "${dynamoSchema}/bin/${dynamoSchema.name}";
    };
    name = "dynamo-etl";
    entrypoint = ./entrypoint.sh;
  }
