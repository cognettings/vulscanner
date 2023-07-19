# For more information visit:
# https://github.com/fluidattacks/makes
{fetchNixpkgs, ...}: let
  nixpkgs = fetchNixpkgs {
    rev = "d505646da5516457d258f88e76f02852e221bc03";
    sha256 = "sha256-9zHrdATX+SsGp/MfDez4CkduP+vixkkkfnY1qQ3mwyk=";
    overlays = [
      (_: super: {
        # Nginx by default tries to use directories owned by root
        # We have to recompile it pointing to the user-space
        nginxLocal = super.nginx.overrideAttrs (attrs: {
          configureFlags =
            attrs.configureFlags
            ++ [
              "--error-log-path=/tmp/error.log"
              "--http-client-body-temp-path=/tmp/nginx_client_body"
              "--http-fastcgi-temp-path=/tmp/nginx_fastcgi"
              "--http-log-path=/tmp/access.log"
              "--http-proxy-temp-path=/tmp/nginx_proxy"
              "--http-scgi-temp-path=/tmp/nginx_scgi"
              "--http-uwsgi-temp-path=/tmp/nginx_uwsgi"
            ];
        });
      })
    ];
  };
in {
  cache = {
    readNixos = true;
    extra = {
      fluidattacks = {
        enable = true;
        pubKey = "fluidattacks.cachix.org-1:upiUCP8kWnr7NxVSJtTOM+SBqL0pZhZnUoqPG04sBv0=";
        token = "CACHIX_AUTH_TOKEN";
        type = "cachix";
        url = "https://fluidattacks.cachix.org";
        write = true;
      };
    };
  };
  extendingMakesDirs = ["/"];
  formatBash = {
    enable = true;
    targets = ["/"];
  };
  formatMarkdown = {
    enable = true;
    doctocArgs = ["--title" "# Contents"];
    targets = ["/skims/LICENSE.md"];
  };
  formatNix = {
    enable = true;
    targets = ["/"];
  };
  formatPython = {
    default = {
      targets = ["/"];
    };
  };
  formatTerraform = {
    enable = true;
    targets = ["/"];
  };
  formatYaml = {
    enable = true;
    targets = ["/"];
  };
  lintBash = {
    enable = true;
    targets = ["/"];
  };
  lintGitCommitMsg = {
    branch = "trunk";
    enable = true;
    config = "/.lint-git-commit-msg/config.js";
    parser = "/.lint-git-commit-msg/parser.js";
  };
  lintGitMailMap = {
    enable = true;
  };
  lintNix = {
    enable = true;
    targets = ["/"];
  };
  lintTerraform = {
    config = "/.lint-terraform.hcl";
  };
  imports = [
    ./airs/makes.nix
    ./common/makes.nix
    ./docs/makes.nix
    ./integrates/forces/makes.nix
    ./integrates/makes.nix
    ./melts/makes.nix
    ./observes/makes.nix
    ./skims/makes.nix
    ./sorts/makes.nix
  ];
  inputs = {
    inherit nixpkgs;
    flakeAdapter = import (builtins.fetchTarball {
      url = "https://github.com/edolstra/flake-compat/archive/12c64ca55c1014cdc1b16ed5a804aa8576601ff2.tar.gz";
      sha256 = "0jm6nzb83wa6ai17ly9fzpqc40wg1viib8klq8lby54agpl213w5";
    });
    makeImpureCmd = {
      cmd,
      path,
    }:
      nixpkgs.runCommandLocal "${cmd}-impure" {
        __impureHostDeps = [path];
      } ''
        if ! [ -x ${path} ]; then
          echo Cannot find command ${path}
          exit 1
        fi
        mkdir -p $out/bin
        ln -s ${path} $out/bin
        manpage="/usr/share/man/man1/${cmd}.1"
        if [ -f $manpage ]; then
          mkdir -p $out/share/man/man1
          ln -s $manpage $out/share/man/man1
        fi
      '';
  };
  testLicense = {
    enable = true;
  };
}
