{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  replace = {
    __argSetupRetrievesDevRuntime__ =
      outputs."/common/utils/retrieves/config/dev-runtime";
    __argSetupRetrievesWebviewRuntime__ =
      outputs."/common/utils/retrieves/config/webview-runtime";
    __argSecretsProd__ = projectPath "/common/secrets/prod.yaml";
  };
  entrypoint = ./entrypoint.sh;
  name = "retrieves-deploy";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-18_x
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/retrieves/config/dev-runtime-env"
      outputs."/common/utils/sops"
    ];
  };
}
