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

  fa-purity = import ./fa_purity.nix {inherit nixpkgs;};
  fa-singer-io = import ./fa_singer_io.nix {inherit fa-purity nixpkgs;};

  layer_1 = python_pkgs:
    python_pkgs
    // {
      fa-purity = fa-purity."${python_version}".pkg;
      fa-singer-io = fa-singer-io."${python_version}".pkg;
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
