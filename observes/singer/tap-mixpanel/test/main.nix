{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-tap-mixpanel-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.mixpanel.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.mixpanel.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
