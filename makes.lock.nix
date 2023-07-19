{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/heads/main";
    rev = "91ee9fef013a9e3ad31fa4aac504eb62fd9639d1";
  };
}
