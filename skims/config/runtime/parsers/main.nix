{inputs, ...}:
inputs.nixpkgs.stdenv.mkDerivation {
  buildPhase = ''
    export envTreeSitterCSharp="${inputs.skimsTreeSitterCSharp}"
    export envTreeSitterDart="${inputs.skimsTreeSitterDart}"
    export envTreeSitterGo="${inputs.skimsTreeSitterGo}"
    export envTreeSitterHcl="${inputs.skimsTreeSitterHcl}"
    export envTreeSitterJava="${inputs.skimsTreeSitterJava}"
    export envTreeSitterJavaScript="${inputs.skimsTreeSitterJavaScript}"
    export envTreeSitterJson="${inputs.skimsTreeSitterJson}"
    export envTreeSitterKotlin="${inputs.skimsTreeSitterKotlin}"
    export envTreeSitterPhp="${inputs.skimsTreeSitterPhp}"
    export envTreeSitterPython="${inputs.skimsTreeSitterPython}"
    export envTreeSitterRuby="${inputs.skimsTreeSitterRuby}"
    export envTreeSitterScala="${inputs.skimsTreeSitterScala}"
    export envTreeSitterSwift="${inputs.skimsTreeSitterSwift}"
    export envTreeSitterTsx="${inputs.skimsTreeSitterTsx}"
    export envTreeSitterYaml="${inputs.skimsTreeSitterYaml}"

    python build.py
  '';
  name = "skims-config-runtime-parsers";
  nativeBuildInputs = [
    # This is the tree_sitter version used for compiling all parsers.
    # Please make sure to use the same version as specified in
    # skims/config/runtime/pypi/deps.yaml
    # for compatibility.
    inputs.nixpkgs.python311Packages.tree-sitter
  ];
  src = ./.;
}
