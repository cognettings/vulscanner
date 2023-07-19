{nixpkgs}: let
  python_version = "python311";
  out = import ./build {
    inherit nixpkgs python_version;
  };
in
  out
