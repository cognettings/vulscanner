{
  description = "Dynamo ETLs configuration";
  inputs = {
    nix_filter.url = "github:numtide/nix-filter";
    nixpkgs.url = "github:nixos/nixpkgs?rev=0cd51a933d91078775b300cf0f29aa3495231aa2";
    purity = {
      url = "gitlab:dmurciaatfluid/purity/tags/v1.34.0";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        nix_filter.follows = "nix_filter";
      };
    };
    redshift_client = {
      url = "gitlab:dmurciaatfluid/redshift_client?rev=ebf5ae02eacf7a14c63d3dac26d4de79047e6c52";
      inputs = {
        nix_filter.follows = "nix_filter";
        nixpkgs.follows = "nixpkgs";
        fa-purity.follows = "purity";
      };
    };
  };
  outputs = {
    self,
    nix_filter,
    nixpkgs,
    purity,
    redshift_client,
  }: let
    system = builtins.currentSystem;
    out = python_version:
      import "${self}/build" {
        inherit python_version;
        nixpkgs =
          nixpkgs.legacyPackages."${system}"
          // {
            fa_purity = purity.packages."${system}";
            redshift_client = redshift_client.packages."${system}";
          };
        src = self;
      };
  in {
    packages."${system}" = out "python311";
    defaultPackage."${system}" = self.packages."${system}".pkg;
  };
}
