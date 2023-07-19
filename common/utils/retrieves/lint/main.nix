{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSetupRetrievesDevRuntime__ =
      outputs."/common/utils/retrieves/config/dev-runtime";
  };
  entrypoint = ./entrypoint.sh;
  name = "retrieves-lint-code";
  searchPaths = {
    bin = [inputs.nixpkgs.nodejs-18_x];
    source = [
      outputs."/common/utils/lint-npm-deps"
      outputs."/common/utils/retrieves/config/dev-runtime-env"
    ];
  };
}
