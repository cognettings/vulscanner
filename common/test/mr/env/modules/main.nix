{
  makeNodeJsModules,
  projectPath,
  ...
}:
makeNodeJsModules {
  name = "common-test-mr-env-modules";
  nodeJsVersion = "18";
  packageJson = projectPath "/common/test/mr/package.json";
  packageLockJson = projectPath "/common/test/mr/package-lock.json";
}
