{
  makePythonPypiEnvironment,
  inputs,
  outputs,
  ...
}:
makePythonPypiEnvironment {
  name = "clone-roots";
  searchPathsRuntime = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.openssh
    ];
    source = [
      outputs."/common/utils/git_self"
    ];
  };
  sourcesYaml = ./pypi-sources.yaml;
}
