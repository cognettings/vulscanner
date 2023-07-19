{
  nixpkgs,
  fa-purity,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/singer_io";
    rev = "f37648c274a1378db3b075c711f562ad58cdde10";
    ref = "refs/tags/v1.7.0";
  };
in
  import "${src}/build" {
    inherit src;
    nixpkgs =
      nixpkgs
      // {
        purity = fa-purity;
      };
  }
