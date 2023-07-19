{
  nixpkgs,
  projectPath,
  observesIndex,
}: let
  python_version = "python311";
  out = import ./build {
    inherit python_version;
    inherit nixpkgs;
    src = ./.;
  };
in
  out
