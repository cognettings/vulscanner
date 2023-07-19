{
  makeNodeJsModules,
  projectPath,
  ...
}:
makeNodeJsModules {
  name = "retrieves-webview-runtime";
  nodeJsVersion = "18";
  packageJson = projectPath "/common/utils/retrieves/webview-ui/package.json";
  packageLockJson = projectPath "/common/utils/retrieves/webview-ui/package-lock.json";
}
