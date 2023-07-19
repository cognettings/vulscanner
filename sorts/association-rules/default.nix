{
  pkgs,
  src,
}: let
  python_version = "python39";
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = pkgs."${python_version}".buildEnv.override;
    inherit (pkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (pkgs.python3Packages) fetchPypi;
    inherit (pkgs) fetchFromGitHub;
  };
  python_pkgs = import ./build/deps {
    inherit lib;
    python_pkgs = pkgs."${python_version}Packages";
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}
