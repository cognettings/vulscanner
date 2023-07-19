{
  testPullRequest = {
    modules = {
      default = {
        dangerfile = ./src/dangerfile.ts;
        extraArgs = [
          "--failOnErrors"
          "--config"
          (builtins.toJSON {
            tests = [
              "branchEqualsToUsername"
              "mrMessageEqualsCommitMessage"
              "firstPipelineSuccessful"
              "mrAuthorSyntax"
            ];
          })
        ];
      };
    };
  };
}
