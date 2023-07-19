{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    : && common-test-base \
      && lint-git-commit-msg-for-lint-git-commit-msg \
      && common-test-leaks
  '';
  name = "common-test-hooks-pre-push";
  searchPaths.bin = [
    outputs."/common/test/base"
    outputs."/lintGitCommitMsg"
    outputs."/common/test/leaks"
  ];
}
