{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-test-mr-lint-eslint";
  replace = {
    __argNodeModules__ = outputs."/common/test/mr/env/modules";
  };
  searchPaths = {
    bin = [inputs.nixpkgs.nodejs-18_x];
    source = [
      outputs."/common/test/mr/env/runtime"
    ];
  };
}
