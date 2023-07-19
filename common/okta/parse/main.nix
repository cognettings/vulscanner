{
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argParser__ = projectPath "/common/okta/parse/src/__init__.py";
    __argSopsData__ = projectPath "/common/okta/data.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      inputs.nixpkgs.python39
      inputs.nixpkgs.sops
    ];
    source = [outputs."/common/utils/types_self"];
  };
  template = ./template.sh;
  name = "okta-parse";
}
