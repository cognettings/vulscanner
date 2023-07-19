{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "common-sqs-consumer";
  sourcesYaml = ./pypi-sources.yaml;
}
