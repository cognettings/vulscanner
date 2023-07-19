{
  libGit,
  makeTemplate,
  ...
}:
makeTemplate {
  name = "integrates-deploy-worker-export-repo-variables";
  searchPaths = {
    source = [
      libGit
    ];
  };
  template = ./template.sh;
}
