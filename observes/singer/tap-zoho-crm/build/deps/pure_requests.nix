{
  fa-purity,
  nixpkgs,
  python_version,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/pure_requests";
    rev = "dd42fd1ade92a11baf330ccbf3f937019a69d24d";
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
