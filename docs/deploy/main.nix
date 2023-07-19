{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs-deploy";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      outputs."/docs"
    ];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/cloudflare"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
