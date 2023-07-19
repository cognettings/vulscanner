{
  fa-purity,
  nixpkgs,
  python_version,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "refs/tags/1.2.2+1";
    rev = "ebf5ae02eacf7a14c63d3dac26d4de79047e6c52";
  };
in
  import "${src}/build" {
    inherit python_version src;
    nixpkgs =
      nixpkgs
      // {
        inherit fa-purity;
      };
  }
