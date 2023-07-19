{
  buildPythonPackage,
  metadata,
  pkg_deps,
  src,
}: let
  arch_check = ./check/arch.sh;
  type_check = ./check/types.sh;
  test_check = ./check/tests.sh;
in
  buildPythonPackage {
    inherit src arch_check type_check test_check;
    inherit (metadata) version;
    pname = metadata.name;
    format = "pyproject";
    checkPhase = [
      ''
        source ${arch_check} \
        && source ${type_check} \
        && source ${test_check} \
      ''
    ];
    doCheck = true;
    pythonImportsCheck = [metadata.name];
    nativeBuildInputs = pkg_deps.build_deps;
    propagatedBuildInputs = pkg_deps.runtime_deps;
    nativeCheckInputs = pkg_deps.test_deps;
  }
