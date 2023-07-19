{
  lib,
  src,
  metadata,
  runtime_deps,
}:
lib.buildPythonPackage {
  inherit src;
  pname = metadata.name;
  inherit (metadata) version;
  propagatedBuildInputs = runtime_deps;
  pythonImportsCheck = ["tap_google_sheets"];
  doCheck = false;
}
