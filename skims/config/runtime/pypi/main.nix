{
  inputs,
  makePythonPypiEnvironment,
  ...
}:
makePythonPypiEnvironment rec {
  name = "skims-runtime";
  searchPathsBuild = {
    bin =
      [
        inputs.nixpkgs.curl
        inputs.nixpkgs.gcc
      ]
      ++ inputs.nixpkgs.lib.optionals inputs.nixpkgs.stdenv.isDarwin [
        inputs.nixpkgs.clang
        inputs.nixpkgs.darwin.cctools
        inputs.nixpkgs.libxml2.dev
        inputs.nixpkgs.libxslt.dev
      ];
    export = [
      ["CPATH" inputs.nixpkgs.graphviz "/include"]
      ["LIBRARY_PATH" inputs.nixpkgs.graphviz "/lib"]
    ];
  };
  searchPathsRuntime = searchPathsBuild;
  sourcesYaml = ./sources.yaml;
  withSetuptools_67_7_2 = true;
  withWheel_0_40_0 = true;
}
