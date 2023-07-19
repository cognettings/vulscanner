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
      fa-singer-io
      more-itertools
      mypy-boto3-s3
      pure-requests
      python-dateutil
      requests
      types-boto3
      types-python-dateutil
      types-requests
      utils-logger
    ];
    build_deps = with deps.python_pkgs; [flit-core];
    test_deps = with deps.python_pkgs; [
      import-linter
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
