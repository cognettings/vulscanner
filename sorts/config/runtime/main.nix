{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}: let
  # Needed to properly cross-compile their native extensions
  self_psycopg2 = inputs.nixpkgs.python311Packages.psycopg2;
  pythonRequirements = makePythonPypiEnvironment {
    name = "sorts-runtime";
    searchPathsRuntime.bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
      self_psycopg2
    ];
    searchPathsBuild.bin = [
      inputs.nixpkgs.gcc
      inputs.nixpkgs.postgresql
    ];
    sourcesYaml = ./pypi-sources.yaml;

    withWheel_0_40_0 = true;
  };
in
  makeTemplate {
    replace = {
      __argSrcSortsSorts__ = projectPath "/sorts/sorts";
    };
    name = "sorts-config-runtime";
    searchPaths = {
      rpath = [
        inputs.nixpkgs.gcc.cc.lib
        inputs.nixpkgs.zlib
      ];
      bin = [
        inputs.nixpkgs.git
        inputs.nixpkgs.python311
      ];
      pythonPackage = [
        "${self_psycopg2}/lib/python3.11/site-packages/"
        (projectPath "/sorts/sorts")
        (projectPath "/sorts")
        (projectPath "/common/utils/bugsnag/client")
      ];
      pythonPackage311 = [
        inputs.nixpkgs.python311Packages.numpy
      ];
      source = [
        (makeTemplate {
          replace = {
            __argSortsModel__ = inputs.nixpkgs.fetchurl {
              sha256 = "Xnj4urLBQdn4Ak1DJZeFDM2OumOuc2Xfgtic0K31CgU=";
              url = "https://sorts.s3.amazonaws.com/training-output/model.joblib?versionId=d4ey.sHyTg8f.QK8Wdmb1gZobdXDoHTA";
            };
            __argSrcSortsStatic__ = projectPath "/sorts/static";
          };
          name = "sorts-config-context-file";
          template = ''
            export SORTS_STATIC_PATH='__argSrcSortsStatic__'
            export SORTS_MODEL_PATH='__argSortsModel__'
          '';
        })
        pythonRequirements
      ];
    };
    template = ./template.sh;
  }
