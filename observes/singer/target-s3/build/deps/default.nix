{
  makes_inputs,
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (nixpkgs.python3Packages) fetchPypi;
  };

  utils = import ./override_utils.nix;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  arch-lint = import ./arch_lint.nix {inherit nixpkgs python_version;};
  fa-purity = let
    core = import ./fa_purity.nix {inherit nixpkgs python_version;};
  in {
    "${python_version}" = core;
  };
  fa-singer-io = import ./fa_singer_io.nix {inherit fa-purity nixpkgs python_version;};
  utils-logger = import ./utils_logger.nix {
    inherit fa-purity makes_inputs nixpkgs python_version;
  };

  layer_1 = python_pkgs:
    python_pkgs
    // {
      arch-lint = arch-lint.pkg;
      fa-purity = fa-purity."${python_version}".pkg;
      fa-singer-io = fa-singer-io.pkg;
      mypy-boto3-s3 = import ./boto3/s3-stubs.nix {inherit lib python_pkgs;};
      types-boto3 = import ./boto3/stubs.nix {inherit lib python_pkgs;};
      utils-logger = utils-logger.pkg;
    };

  jsonschema_override = python_pkgs: utils.replace_pkg ["jsonschema"] (import ./jsonschema.nix lib python_pkgs);
  networkx_override = python_pkgs: utils.replace_pkg ["networkx"] (import ./networkx.nix lib python_pkgs);
  overrides = map pkgs_overrides [
    jsonschema_override
    networkx_override
    (_: utils.no_check_override)
  ];

  python_pkgs = utils.compose ([layer_1] ++ overrides) nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
