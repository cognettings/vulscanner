{
  nixpkgs,
  observesIndex,
  projectPath,
}: let
  python_version = "python311";
  makes_inputs = {
    inherit projectPath observesIndex;
  };
  out = import ./build {
    inherit makes_inputs nixpkgs python_version;
    src = ./.;
  };
in
  out
