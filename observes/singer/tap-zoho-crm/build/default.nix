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
      click
      fa-purity
      fa-singer-io
      pure-requests
      redshift-client
      requests
      types-requests
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
