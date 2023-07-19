{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-common-singer-io-test";
  env = {
    envSrc = projectPath inputs.observesIndex.common.singer_io.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/common/singer-io/env/development"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
