{
  makes_inputs,
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage toPythonApplication;
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
  utils-logger = import ./utils_logger.nix {
    inherit fa-purity makes_inputs nixpkgs python_version;
  };

  layer_1 = python_pkgs:
    python_pkgs
    // {
      utils-logger = utils-logger.pkg;
      arch-lint = arch-lint.pkg;
      fa-purity = fa-purity."${python_version}".pkg;
    };

  networkx_override = python_pkgs: utils.replace_pkg ["networkx"] (import ./networkx.nix lib python_pkgs);
  overrides = map pkgs_overrides [
    networkx_override
    (_: utils.no_check_override)
  ];

  new_nixpkgs =
    nixpkgs
    // {
      tap-google-sheets = import ./tap-google-sheets.nix {inherit lib makes_inputs nixpkgs;};
      target-redshift = import ./target-redshift.nix {inherit lib makes_inputs nixpkgs;};
    };
  python_pkgs = utils.compose ([layer_1] ++ overrides) nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
  nixpkgs = new_nixpkgs;
}
