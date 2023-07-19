lib: python_pkgs:
lib.buildPythonPackage rec {
  pname = "mypy-boto3-redshift";
  version = "1.26.79";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "YItvLdDalFh1gOFtUAiloK7tPb+87KomDBNFiB/aguM=";
  };
  nativeBuildInputs = with python_pkgs; [boto3];
  propagatedBuildInputs = with python_pkgs; [botocore typing-extensions];
}
