{
  makes_inputs,
  nixpkgs,
  python_version,
  fa-purity,
}: let
  src = makes_inputs.projectPath makes_inputs.observesIndex.common.utils_logger_2.root;
in
  import src {
    inherit python_version src;
    nixpkgs =
      nixpkgs
      // {
        inherit fa-purity;
      };
  }
