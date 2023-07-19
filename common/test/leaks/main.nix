{
  inputs,
  makeScript,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-test-leaks";
  searchPaths.bin = [
    inputs.nixpkgs.git
    inputs.nixpkgs.gitleaks
    inputs.nixpkgs.gnugrep
  ];
}
