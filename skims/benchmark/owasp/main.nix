{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "skims-benchmark-owasp";
  replace = {
    __argBenchmarkRepo__ = inputs.skimsBenchmarkOwasp;
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.python311
      outputs."/skims"
    ];
    source = [outputs."/skims/config/runtime"];
  };
  entrypoint = ./entrypoint.sh;
}
