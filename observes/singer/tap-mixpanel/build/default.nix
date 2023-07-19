{
  nixpkgs,
  python_version,
  src,
}: let
  deps = import ./deps {
    inherit nixpkgs python_version;
  };
  pkg_deps = {
    runtime_deps = with deps.python_pkgs; [
      boto3
      botocore
      numpy
      pandas
      requests
    ];
    build_deps = with deps.python_pkgs; [flit-core];
    test_deps = with deps.python_pkgs; [
      mypy
      pytest
      pytest-freezegun
    ];
  };
  packages = import ./generic_builder {
    inherit (deps.lib) buildEnv buildPythonPackage;
    inherit nixpkgs pkg_deps src;
  };
in
  packages
