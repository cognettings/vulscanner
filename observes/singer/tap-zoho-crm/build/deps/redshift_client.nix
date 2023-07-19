{
  fa-purity,
  nixpkgs,
  python_version,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "refs/tags/v3.0.0";
    rev = "e53905c94293f6348166fd44f7373608956b6a4c";
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
