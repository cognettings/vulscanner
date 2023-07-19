{nixpkgs}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "feaa69ef3ad93ad91fd679d8169c80458457d779"; # post 1.33.2
    ref = "refs/heads/main";
  };
in
  import "${src}/build" {
    inherit src nixpkgs;
  }
