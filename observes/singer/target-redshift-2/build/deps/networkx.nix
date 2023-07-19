lib: python_pkgs:
python_pkgs.networkx.overridePythonAttrs (
  _: rec {
    version = "2.8.8";
    src = lib.fetchPypi {
      pname = "networkx";
      inherit version;
      hash = "sha256-Iw04gRevhw/OVkejxSQB/PdT6Ucg5uprQZelNVZIiF4=";
    };
  }
)
