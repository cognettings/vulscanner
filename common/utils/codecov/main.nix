{
  __system__,
  inputs,
  makeDerivation,
  ...
}: let
  srcs = {
    aarch64-darwin = {
      url = "https://github.com/codecov/uploader/releases/download/v0.5.0/codecov-macos";
      sha256 = "sha256-zX/v5ln8ff1eLyFrvWGwa5OCjW1J7FzCrwSBAHkf/JE=";
    };
    aarch64-linux = {
      url = "https://github.com/codecov/uploader/releases/download/v0.5.0/codecov-aarch64";
      sha256 = "sha256-I781+5dI0GfuuIgUa7aPSQSCKX9+bI1MBra5sjJ1UbU=";
    };
    x86_64-linux = {
      url = "https://github.com/codecov/uploader/releases/download/v0.5.0/codecov-linux";
      sha256 = "sha256-ArBVQUzBJCA6sGH/xF9Ul8o57eXmOgZxemmBwy17Ql8=";
    };
  };
in
  makeDerivation {
    env.envSrc = inputs.nixpkgs.fetchurl srcs.${__system__};
    builder = ''
      mkdir -p $out/bin
      copy $envSrc $out/bin/codecov
      chmod +x $out/bin/codecov
    '';
    name = "codecov";
  }
