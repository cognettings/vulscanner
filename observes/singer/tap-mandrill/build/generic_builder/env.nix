{
  buildEnv,
  pkg_deps,
  pkg,
}: let
  build_env = extraLibs:
    buildEnv {
      inherit extraLibs;
      ignoreCollisions = false;
    };
in {
  runtime = build_env [pkg];
  dev = build_env (pkg_deps.runtime_deps ++ pkg_deps.test_deps);
}
