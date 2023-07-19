{
  inputs,
  projectPath,
  makeDynamoDb,
  makeScript,
  ...
}: let
  dynamodb_data = makeScript {
    replace = {
      __argDbData__ = projectPath "/integrates/back/test/data";
      __argIntegratesVmsDbDesign__ = projectPath "/integrates/arch/database-design.json";
      __argAsyncProcessingDbDesign__ = projectPath "/integrates/back/src/batch/fi_async_processing-design.json";
      __argMailMap__ = projectPath "/.mailmap";
    };
    name = "data-for-db";
    searchPaths = {
      bin = [
        inputs.nixpkgs.awscli
        inputs.nixpkgs.git
        inputs.nixpkgs.gnugrep
        inputs.nixpkgs.gnused
        inputs.nixpkgs.jq
      ];
    };
    entrypoint = ./data.sh;
  };
  dynamodb = makeDynamoDb {
    name = "db";
    host = "0.0.0.0";
    port = "8022";
    infra = projectPath "/integrates/db/dynamodb/infra";
    data = ["integrates/db/.data"];
    daemonMode = false;
  };
in
  makeScript {
    name = "dynamodb";
    searchPaths = {
      bin = [
        dynamodb_data
        dynamodb
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
