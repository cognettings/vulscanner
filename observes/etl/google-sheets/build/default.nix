{
  makes_inputs,
  nixpkgs,
  python_version,
  src,
}: let
  deps = import ./deps {
    inherit makes_inputs nixpkgs python_version;
  };
  bin_deps = [
    deps.nixpkgs.tap-google-sheets
    deps.nixpkgs.target-redshift
    deps.nixpkgs.sops
  ];
  pkg_deps = {
    inherit bin_deps;
    runtime_deps =
      bin_deps
      ++ (with deps.python_pkgs; [
        fa-purity
        utils-logger
      ]);
    build_deps = with deps.python_pkgs; [flit-core];
    test_deps = with deps.python_pkgs; [
      arch-lint
      mypy
      pylint
      pytest
    ];
  };
  packages = import ./generic_builder {
    inherit (deps.lib) buildEnv buildPythonPackage;
    inherit (deps) nixpkgs;
    inherit pkg_deps src;
  };
in
  packages // {inherit (pkg_deps) bin_deps;}
