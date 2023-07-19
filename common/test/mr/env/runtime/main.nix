{
  makeNodeJsEnvironment,
  projectPath,
  ...
}:
makeNodeJsEnvironment {
  name = "common-test-mr-env-runtime";
  nodeJsVersion = "18";
  packageJson = projectPath "/common/test/mr/package.json";
  packageLockJson = projectPath "/common/test/mr/package-lock.json";
}
