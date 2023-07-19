{
  makeNodeJsEnvironment,
  makeScript,
  ...
}: let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "bugsnag-announce";
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    entrypoint = ./entrypoint.sh;
    name = "bugsnag-announce";
    searchPaths.source = [nodeJsEnvironment];
  }
