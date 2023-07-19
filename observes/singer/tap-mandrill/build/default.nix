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
      click
      fa-purity
      fa-singer-io
      mailchimp-transactional
      python-dateutil
      requests
      types-requests
      types-dateutil
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
