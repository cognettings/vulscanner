{
  makes_inputs,
  nixpkgs,
  python_version,
  src,
}: let
  deps = import ./deps {
    inherit makes_inputs nixpkgs python_version;
  };
  pkg_deps = {
    runtime_deps = with deps.python_pkgs; [
      boto3
      click
      fa-purity
      mypy-boto3-dynamodb
      types-boto3
      utils-logger
    ];
    build_deps = with deps.python_pkgs; [flit-core];
    test_deps = with deps.python_pkgs; [
      arch-lint
      mypy
      pytest
    ];
  };
  packages = import ./generic_builder {
    inherit (deps.lib) buildEnv buildPythonPackage;
    inherit nixpkgs pkg_deps src;
  };
in
  packages
