{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-test-mr-lint";
  searchPaths.bin = [
    outputs."/common/test/mr/lint/deps"
    outputs."/common/test/mr/lint/eslint"
  ];
}
