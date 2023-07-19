{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-test-mr-lint-deps";
  searchPaths.source = [outputs."/common/utils/lint-npm-deps"];
}
