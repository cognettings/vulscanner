{
  pkgs,
  local_pkgs,
  python_version,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = pkgs."${python_version}".buildEnv.override;
    inherit (pkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (pkgs.python3Packages) fetchPypi;
  };
  python_pkgs = import ./build/deps {
    inherit pkgs lib local_pkgs python_version;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
in
  self_pkgs
