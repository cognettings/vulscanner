{
  makePythonPypiEnvironment,
  inputs,
  ...
}:
makePythonPypiEnvironment {
  name = "integrates-back-unit-tests";
  searchPathsBuild = {
    bin = [inputs.nixpkgs.gcc];
  };
  searchPathsRuntime = {
    bin = [inputs.nixpkgs.gcc];
  };
  sourcesYaml = ./pypi-sources.yaml;
  withSetuptools_67_7_2 = true;
  withWheel_0_40_0 = true;
}
