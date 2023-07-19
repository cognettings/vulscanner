{
  libGit,
  makeTemplate,
  outputs,
  inputs,
  ...
}:
makeTemplate {
  name = "integrates-deploy-worker-export-repo-variables";
  searchPaths = {
    bin = [inputs.nixpkgs.utillinux];
    source = [
      libGit
      outputs."/integrates/back/deploy/lib"
    ];
  };
  template = ./template.sh;
}
