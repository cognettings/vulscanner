{
  makeTemplate,
  makePythonPypiEnvironment,
  outputs,
  projectPath,
  inputs,
  ...
}: let
  # Needed to properly cross-compile their native extensions
  self_psycopg2 = inputs.nixpkgs.python311Packages.psycopg2;
  self_pycurl = inputs.nixpkgs.python311Packages.pycurl;
  self_python_magic = inputs.nixpkgs.python311Packages.python_magic;

  pythonRequirements = makePythonPypiEnvironment {
    name = "integrates-back-runtime";
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
        inputs.nixpkgs.gnutar
        inputs.nixpkgs.gzip
        inputs.nixpkgs.postgresql
        self_psycopg2
        self_pycurl
        self_python_magic
      ];
    };
    withSetuptools_67_7_2 = true;
    withWheel_0_40_0 = true;
  };
in
  makeTemplate {
    name = "integrates-back-pypi-runtime";
    searchPaths = {
      pythonPackage = [
        "${self_psycopg2}/lib/python3.11/site-packages/"
        "${self_pycurl}/lib/python3.11/site-packages/"
        "${self_python_magic}/lib/python3.11/site-packages/"
        (projectPath "/integrates/back/src")
        (projectPath "/integrates")
        (projectPath "/common/utils/bugsnag/client")
      ];
      source = [
        pythonRequirements
        outputs."/common/utils/serializers"
        outputs."/common/utils/git_self"
        outputs."/common/utils/async_sqs_consummer"
        outputs."/common/utils/async_sqs_consummer/env/pypi/runtime"
      ];
    };
  }
