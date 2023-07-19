{
  lib,
  src,
  metadata,
  propagatedBuildInputs,
  nativeBuildInputs,
}:
lib.buildPythonPackage rec {
  pname = metadata.name;
  inherit (metadata) version;
  format = "pyproject";
  type_check = ./check/types.sh;
  installCheckPhase = [
    ''
      source ${type_check}
    ''
  ];
  doCheck = true;
  pythonImportsCheck = [pname];
  inherit src propagatedBuildInputs nativeBuildInputs;
}
