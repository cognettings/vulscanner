{
  fa-purity,
  nixpkgs,
  python_version,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/pure_requests";
    rev = "c9167f49fd1f664d6c7977abbfa2dd108465332d";
    ref = "refs/heads/main";
  };
in
  import "${src}/build" {
    inherit src python_version;
    nixpkgs =
      nixpkgs
      // {
        inherit fa-purity;
      };
  }
