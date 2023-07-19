{
  makeScript,
  makePythonPypiEnvironment,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argCleanRepositoryBranches__ = projectPath "/common/dev/clean/branches/src/__init__.py";
  };
  name = "common_dev_clean_branches";
  entrypoint = ./entrypoint.sh;
  searchPaths = {
    source = [
      (makePythonPypiEnvironment
        {
          name = "clean-gitlab-universe-branches";
          sourcesYaml = ./pypi-sources.yaml;
        })
    ];
  };
}
