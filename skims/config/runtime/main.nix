{
  inputs,
  makeTemplate,
  projectPath,
  outputs,
  ...
}: let
  self_bugsnag = inputs.nixpkgs.python311Packages.bugsnag.overridePythonAttrs (_: rec {
    src =
      builtins.fetchGit
      {
        url = "https://github.com/fluidattacks/bugsnag-python";
        ref = "master";
        rev = "41387bcff4ae94ae633725889cb55567bcce5c9e";
      };
    doCheck = false;
  });
in
  makeTemplate {
    replace = {
      __argSrcSkimsSkims__ = projectPath "/skims/skims";
    };
    name = "skims-config-runtime";
    searchPaths = {
      bin = [
        inputs.nixpkgs.gcc
        inputs.nixpkgs.git
        inputs.nixpkgs.graphviz
        inputs.nixpkgs.wget
      ];
      pythonPackage = [
        "${self_bugsnag}/lib/python3.11/site-packages/"
        (projectPath "/skims/skims")
        (projectPath "/common/utils/bugsnag/client")
      ];
      source = [
        outputs."/common/utils/safe-pickle"
        outputs."/common/utils/serializers"
        outputs."/skims/config/runtime/pypi"
        (makeTemplate {
          replace = {
            __argCriteriaRequirements__ =
              projectPath "/common/criteria/src/requirements/data.yaml";
            __argCriteriaVulnerabilities__ =
              projectPath "/common/criteria/src/vulnerabilities/data.yaml";
            __argSkimsLegal__ =
              projectPath "/skims/LEGAL.md";
            __argSrcTreeSitterParsers__ = outputs."/skims/config/runtime/parsers";
            __argSrcSkimsStatic__ = projectPath "/skims/static";
            __argSkimsDbDesign__ = projectPath "/skims/arch/database-design.json";
          };
          name = "skims-config-context-file";
          template = ''
            # There is no problem in making this key public
            #   it's intentional so we can monitor Skims stability in remote users
            export BUGSNAG_API_KEY=f990c9a571de4cb44c96050ff0d50ddb
            export SKIMS_CIPHER_SUITES_PATH='__argSrcSkimsStatic__/cryptography/cipher_suites.csv'
            export SKIMS_CRITERIA_REQUIREMENTS='__argCriteriaRequirements__'
            export SKIMS_CRITERIA_VULNERABILITIES='__argCriteriaVulnerabilities__'
            export SKIMS_LEGAL='__argSkimsLegal__'
            export SKIMS_STATIC='__argSrcSkimsStatic__'
            export SKIMS_TREE_SITTER_PARSERS='__argSrcTreeSitterParsers__'
            export SKIMS_DB_MODEL_PATH='__argSkimsDbDesign__'
          '';
        })
      ];
    };
    template = ./template.sh;
  }
