{
  nixpkgs,
  python_version,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "1816e0d8d95eb0c115d67dbc19d8e460edab3911";
    ref = "refs/tags/v1.34.0";
  };
in
  import "${src}/build" {
    inherit src nixpkgs python_version;
  }
