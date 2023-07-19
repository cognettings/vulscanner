{
  nixpkgs,
  python_version,
}: let
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    inherit (nixpkgs."${python_version}".pkgs) buildPythonPackage;
    inherit (nixpkgs.python3Packages) fetchPypi;
    inherit (nixpkgs) fetchFromGitHub;
  };

  utils = import ./override_utils.nix;
  pkgs_overrides = override: python_pkgs: builtins.mapAttrs (_: override python_pkgs) python_pkgs;

  layer_1 = python_pkgs:
    python_pkgs
    // {
      poetry = let
        platformdirs = python_pkgs.platformdirs.overridePythonAttrs (
          old: rec {
            version = "2.6.2";
            SETUPTOOLS_SCM_PRETEND_VERSION = version;
            src = nixpkgs.fetchFromGitHub {
              owner = old.pname;
              repo = old.pname;
              rev = "refs/tags/${version}";
              hash = "sha256-yGpDAwn8Kt6vF2K2zbAs8+fowhYQmvsm/87WJofuhME=";
            };
          }
        );
        poetry-core = python_pkgs.poetry-core.overridePythonAttrs (
          old: rec {
            version = "1.5.2";
            src = nixpkgs.fetchFromGitHub {
              owner = "python-poetry";
              repo = old.pname;
              rev = version;
              hash = "sha256-GpZ0vMByHTu5kl7KrrFFK2aZMmkNO7xOEc8NI2H9k34=";
            };
          }
        );
        installer = python_pkgs.installer.overridePythonAttrs (
          old: rec {
            version = "0.7.0";
            src = lib.fetchFromGitHub {
              owner = "pradyunsg";
              repo = old.pname;
              rev = version;
              hash = "sha256-thHghU+1Alpay5r9Dc3v7ATRFfYKV8l9qR0nbGOOX/A=";
            };
          }
        );
        jeepney = python_pkgs.jeepney.overridePythonAttrs (
          old: rec {
            buildInputs = with python_pkgs; [python_pkgs.outcome python_pkgs.trio];
          }
        );
        pkg = lib.buildPythonPackage rec {
          pname = "poetry";
          version = "1.4.2";
          format = "pyproject";

          src = nixpkgs.fetchFromGitHub {
            owner = "python-poetry";
            repo = pname;
            rev = "refs/tags/${version}";
            hash = "sha256-AiRQFZA5+M1niTzj1RO2lx0QFOMmSzpQo1gzauyTblg=";
          };

          propagatedBuildInputs = with python_pkgs; [
            build
            cachecontrol
            cleo
            crashtest
            dulwich
            filelock
            html5lib
            installer
            jsonschema
            keyring
            lockfile
            packaging
            pexpect
            pkginfo
            platformdirs
            poetry-core
            poetry-plugin-export
            pyproject-hooks
            requests
            requests-toolbelt
            shellingham
            tomlkit
            trove-classifiers
            urllib3
            virtualenv
            xattr
          ];
          nativeCheckInputs = with python_pkgs; [
            cachy
            deepdiff
            flatdict
            pytestCheckHook
            httpretty
            pytest-mock
            pytest-xdist
          ];
        };
        overrides = [
          (utils.replace_pkg ["platformdirs"] platformdirs)
          (utils.replace_pkg ["jeepney"] jeepney)
        ];
      in
        utils.compose overrides pkg;
    };
  layer_2 = python_pkgs:
    python_pkgs
    // {
      backoff = python_pkgs.backoff.overridePythonAttrs (
        old: rec {
          version = "1.8.0";
          src = lib.fetchFromGitHub {
            owner = "litl";
            repo = old.pname;
            rev = "refs/tags/v${version}";
            sha256 = "XI1LL7k3+G2yeMIKuXo4rhfapUd3gI6BfnpgQvWzl1U=";
          };
          nativeBuildInputs = [
            python_pkgs.poetry
          ];
        }
      );
      urllib3 = python_pkgs.urllib3.overridePythonAttrs (
        old: rec {
          version = "1.25.11";
          src = lib.fetchPypi {
            inherit version;
            inherit (old) pname;
            sha256 = "jX6qWoKhysIyFkmQ8Eh0xZTJRT7FXu8C6riFqgL8F6I=";
          };
        }
      );
      idna = python_pkgs.idna.overridePythonAttrs (
        old: rec {
          version = "2.8";
          src = lib.fetchPypi {
            inherit version;
            inherit (old) pname;
            sha256 = "w1ez9ijPU64sTAVifsxIRVMULKIyZOWT0ye83l6cNAc=";
          };
          buildInputs = [python_pkgs.setuptools];
        }
      );
      chardet = python_pkgs.chardet.overridePythonAttrs (
        old: rec {
          version = "3.0.4";
          src = lib.fetchPypi {
            inherit version;
            inherit (old) pname;
            sha256 = "hKuS7RxNTxaRbgWQa2t1psD7XbghzGXnDL1ko+Kl6q4=";
          };
          doCheck = false;
        }
      );
      jsonschema = python_pkgs.jsonschema.overridePythonAttrs (
        old: rec {
          version = "2.6.0";
          src = lib.fetchPypi {
            inherit version;
            inherit (old) pname;
            sha256 = "b/XzGAhwg2yuQPBvoQQZ9VcggXXxOte8Jsqne+sfbgI=";
          };
          propagatedBuildInputs = old.propagatedBuildInputs ++ (with python_pkgs; [vcversioner]);
          doCheck = false;
        }
      );
      simplejson = python_pkgs.simplejson.overridePythonAttrs (
        old: rec {
          version = "3.11.1";
          src = lib.fetchPypi {
            inherit version;
            inherit (old) pname;
            sha256 = "AaItSd3ZoWixNvJsrIfZozVmDOB6pcYwuONgfW9DJec=";
          };
        }
      );
    };
  layer_3 = python_pkgs:
    python_pkgs
    // {
      requests = python_pkgs.requests.overridePythonAttrs (
        old: rec {
          version = "2.22.0";
          src = lib.fetchPypi {
            inherit version;
            inherit (old) pname;
            sha256 = "EeAHqKKqAyP1qSHp5qLX5OZ9mHfoV3P7qbpkGQJcvrQ=";
          };
          propagatedBuildInputs = with python_pkgs; [
            certifi
            chardet
            idna
            urllib3
          ];
          doCheck = false;
        }
      );

      singer-python = python_pkgs.buildPythonPackage rec {
        pname = "singer-python";
        version = "5.12.2";
        propagatedBuildInputs = with python_pkgs; [
          backoff
          ciso8601
          jsonschema
          pytz
          python-dateutil
          simplejson
        ];
        src = lib.fetchPypi {
          inherit pname version;
          sha256 = "xciOZEz1t1oEdGLtE8hoalvoIluHfbhxiX/pUqMXAD8=";
        };
        doCheck = false;
      };
    };

  backoff_override = python_pkgs: utils.replace_pkg ["backoff"] python_pkgs.backoff;
  urllib3_override = python_pkgs: utils.replace_pkg ["urllib3"] python_pkgs.urllib3;
  idna_override = python_pkgs: utils.replace_pkg ["idna"] python_pkgs.idna;
  requests_override = python_pkgs: utils.replace_pkg ["requests"] python_pkgs.requests;
  simplejson_override = python_pkgs: utils.replace_pkg ["simplejson"] python_pkgs.simplejson;
  chardet_override = python_pkgs: utils.replace_pkg ["chardet"] python_pkgs.chardet;
  singer_python_override = python_pkgs: utils.replace_pkg ["singer_python"] python_pkgs.singer-python;

  overrides = map pkgs_overrides [
    backoff_override
    urllib3_override
    idna_override
    requests_override
    simplejson_override
    chardet_override
    singer_python_override
    (_: utils.no_check_override)
  ];
  python_pkgs = utils.compose ([layer_1 layer_2 layer_3] ++ overrides) nixpkgs."${python_version}Packages";
in {
  inherit lib python_pkgs;
}
