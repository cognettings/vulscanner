{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "common-ci-infra-module-inspector";
  sourcesYaml = ./pypi-sources.yaml;
}
