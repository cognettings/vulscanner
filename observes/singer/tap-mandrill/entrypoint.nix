{
  nixpkgs,
  projectPath,
  observesIndex,
}: let
  python_version = "python311";

  arch-lint = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/arch_lint";
      rev = "258b92624e9e2de13f6cafb951f30416eb8e2441"; # post v2.3.0
      ref = "refs/heads/main";
    };
  in
    import "${src}/build" {
      inherit src nixpkgs;
    };

  fa-purity = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/purity";
      rev = "a89d23efd5ee2b2b49b951f187448a1afc6565a3";
      ref = "refs/tags/v1.33.2";
    };
  in
    import "${src}/build" {
      inherit src nixpkgs;
    };

  fa-singer-io = let
    src = builtins.fetchGit {
      url = "https://gitlab.com/dmurciaatfluid/singer_io";
      rev = "75826706c6fc273dc18e13a2771a3cd922d3fea5";
      ref = "refs/tags/v1.6.2";
    };
  in
    import "${src}/build" {
      inherit src;
      nixpkgs =
        nixpkgs
        // {
          purity = fa-purity;
        };
    };

  utils-logger."${python_version}" = let
    src = projectPath observesIndex.common.utils_logger_2.root;
  in
    import src {
      inherit python_version src;
      nixpkgs =
        nixpkgs
        // {
          inherit fa-purity;
        };
    };

  extras = {
    inherit arch-lint fa-purity fa-singer-io utils-logger;
  };
  out = import ./build {
    inherit python_version;
    nixpkgs = nixpkgs // extras;
    src = ./.;
  };
in
  out
