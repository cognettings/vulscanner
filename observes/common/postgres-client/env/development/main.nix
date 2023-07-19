{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-common-postgres-client-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-common-postgres-client-env-development";
        searchPathsBuild.bin = [inputs.nixpkgs.gcc];
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/postgres-client/env/runtime"
    ];
  };
}
