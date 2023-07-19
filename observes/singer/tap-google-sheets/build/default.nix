{
  nixpkgs,
  python_version,
}: let
  metadata = {
    name = "tap-google-sheets";
    version = "2.0.0";
  };
  deps = import ./deps {
    inherit nixpkgs python_version;
  };
  self_pkgs = import ./pkg {
    inherit metadata;
    inherit (deps) lib;
    inherit (deps) python_pkgs;
  };
in
  self_pkgs
