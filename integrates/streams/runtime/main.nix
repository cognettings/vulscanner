{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  ...
}: let
  # Needed to properly cross-compile their native extensions
  self_psycopg2 = inputs.nixpkgs.python311Packages.psycopg2;
  self_pycurl = inputs.nixpkgs.python311Packages.pycurl;

  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-streams-runtime";
    sourcesYaml = ./pypi-sources.yaml;
    searchPathsBuild = {
      bin =
        [
          inputs.nixpkgs.gcc
          inputs.nixpkgs.postgresql
        ]
        ++ inputs.nixpkgs.lib.optionals inputs.nixpkgs.stdenv.isDarwin [
          inputs.nixpkgs.clang
          inputs.nixpkgs.darwin.cctools
        ];
    };
    searchPathsRuntime = {
      bin = [
        inputs.nixpkgs.postgresql
        self_psycopg2
        self_pycurl
      ];
    };
  };
  amazon_kclpy = outputs."/integrates/streams/runtime/amazon_kclpy";
  amazon_kclpy_package = "${amazon_kclpy}/lib/python3.11/site-packages";
in
  makeTemplate {
    name = "integrates-streams-runtime";
    searchPaths = {
      pythonPackage = [
        "${self_psycopg2}/lib/python3.11/site-packages/"
        "${self_pycurl}/lib/python3.11/site-packages/"
        amazon_kclpy_package
      ];
      source = [
        pythonRequirements
      ];
    };
    template = ''
      export CLASSPATH="${amazon_kclpy_package}/amazon_kclpy/jars/*"
    '';
  }
