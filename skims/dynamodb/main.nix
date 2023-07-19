{
  inputs,
  projectPath,
  makeDynamoDb,
  makeScript,
  ...
}: let
  dynamodb_data = makeScript {
    replace = {
      __argSkimsDbDesign__ = projectPath "/skims/arch/database-design.json";
    };
    name = "data-for-db";
    searchPaths = {
      bin = [
        inputs.nixpkgs.awscli
        inputs.nixpkgs.git
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
    infra = projectPath "/skims/dynamodb/infra/";
    data = ["skims/dynamodb/.data"];
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
