{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "observes-singer-tap-mixpanel-env-development";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-mixpanel-env-development";
        sourcesYaml = ./pypi-sources.yaml;
        withWheel_0_40_0 = true;
        withSetuptools_67_7_2 = true;
      })
      outputs."${inputs.observesIndex.tap.mixpanel.env.runtime}"
    ];
  };
}
