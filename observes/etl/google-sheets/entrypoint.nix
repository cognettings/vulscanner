{
  nixpkgs,
  projectPath,
  observesIndex,
}: let
  python_version = "python311";
  nix-filter = let
    src = builtins.fetchGit {
      url = "https://github.com/numtide/nix-filter";
      rev = "fc282c5478e4141842f9644c239a41cfe9586732";
    };
  in
    import src;
  makes_inputs = {
    inherit projectPath observesIndex;
  };
  out = import ./build {
    inherit makes_inputs nixpkgs python_version;
    src = nix-filter {
      root = ./.;
      include = [
        "google_sheets_etl"
        "tests"
        "pyproject.toml"
        "mypy.ini"
        "secrets"
      ];
    };
  };
in
  out
