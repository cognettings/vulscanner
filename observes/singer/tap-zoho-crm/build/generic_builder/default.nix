{
  buildEnv,
  buildPythonPackage,
  nixpkgs,
  pkg_deps,
  src,
}: let
  metadata = import ./metadata.nix src;
  pkg = import ./pkg {
    inherit buildPythonPackage metadata pkg_deps src;
  };
  env = import ./env.nix {
    inherit buildEnv pkg_deps pkg;
  };
  checks = import ./check.nix {inherit pkg;};
in {
  inherit pkg env;
  check = checks;
}
