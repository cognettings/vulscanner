{
  inputs,
  makeScript,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "common-test-base";
  searchPaths.bin = [
    inputs.nixpkgs.gawk
    inputs.nixpkgs.git
    inputs.nixpkgs.gnugrep
    inputs.nixpkgs.gnupg
    inputs.nixpkgs.openssh
  ];
}
