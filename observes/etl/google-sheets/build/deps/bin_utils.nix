{
  wrap_binary = {
    name,
    binary,
    nixpkgs,
  }:
    builtins.derivation {
      inherit name binary;
      utils = nixpkgs.coreutils;
      args = [
        (builtins.toFile "wrap-binary" ''
          export PATH="$PATH:$utils/bin"
          mkdir -p $out/bin
          cp $binary $out/bin
        '')
      ];
      builder = "${nixpkgs.bash}/bin/bash";
      outputs = ["out"];
      system = builtins.currentSystem;
    };
}
