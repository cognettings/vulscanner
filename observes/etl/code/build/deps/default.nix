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
  redshift-client = import ./redshift_client.nix {inherit fa-purity nixpkgs python_version;};
  utils-logger = import ./utils_logger.nix {
    inherit fa-purity makes_inputs nixpkgs python_version;
  };

  layer_1 = python_pkgs:
    python_pkgs
    // {
      arch-lint = arch-lint.pkg;
      fa-purity = fa-purity."${python_version}".pkg;
      gql = python_pkgs.gql.overridePythonAttrs (
        old: {
          propagatedBuildInputs = old.propagatedBuildInputs ++ [python_pkgs.requests-toolbelt];
        }
      );
      pathos = import ./pathos {
        inherit lib python_pkgs;
      };
      redshift-client = redshift-client.pkg;
      types-boto3 = import ./boto3/stubs.nix lib python_pkgs;
      utils-logger = utils-logger.pkg;
    };

  overrides = map pkgs_overrides [
    (_: utils.no_check_override)
  ];

  python_pkgs = utils.compose ([layer_1] ++ overrides) nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
