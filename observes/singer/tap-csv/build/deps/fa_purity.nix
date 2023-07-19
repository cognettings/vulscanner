{
  nixpkgs,
  python_version,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "fefaa689996e468f6adb2bcd6961dcd85509fbf1";
    ref = "refs/tags/v1.37.0";
  };
in
  import "${src}/build" {
    inherit src nixpkgs python_version;
  }
