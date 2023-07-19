{
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

  layer_1 = python_pkgs:
    python_pkgs
    // {
      # requests = import ./requests {inherit lib python_pkgs;};
      types-requests = import ./requests/stubs.nix {inherit lib python_pkgs;};
      # pytz = import ./pytz lib python_pkgs;
      arch-lint = nixpkgs.arch-lint."${python_version}".pkg;
      fa-purity = nixpkgs.fa-purity."${python_version}".pkg;
      fa-singer-io = nixpkgs.fa-singer-io."${python_version}".pkg;
      mailchimp-transactional = import ./mailchimp-transactional {
        inherit lib python_pkgs;
      };
      utils-logger = nixpkgs.utils-logger."${python_version}".pkg;
    };

  jsonschema_override = python_pkgs: utils.replace_pkg ["jsonschema"] (import ./jsonschema.nix lib python_pkgs);
  networkx_override = python_pkgs: utils.replace_pkg ["networkx"] (import ./networkx.nix lib python_pkgs);
  overrides = map pkgs_overrides [
    jsonschema_override
    networkx_override
    (_: utils.no_check_override)
  ];

  final_nixpkgs = utils.compose ([layer_1] ++ overrides) nixpkgs."${python_version}Packages";
in {
  inherit lib;
  python_pkgs = final_nixpkgs;
}
