{
  inputs,
  makeNodeJsVersion,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs";
  searchPaths = {
    bin =
      [
        inputs.nixpkgs.bash
        inputs.nixpkgs.xdg_utils
        outputs."/docs/generate/criteria"
        outputs."/docs/generate/graphs"
        (makeNodeJsVersion "16")
      ]
      ++ inputs.nixpkgs.lib.optionals inputs.nixpkgs.stdenv.isDarwin [
        inputs.nixpkgs.gnugrep
        inputs.nixpkgs.procps
        # Pending contribution
        # https://github.com/NixOS/nixpkgs/blob/master/pkgs/os-specific/darwin/impure-cmds/default.nix
        (inputs.makeImpureCmd {
          cmd = "open";
          path = "/usr/bin/open";
        })
      ];
  };
  entrypoint = ./entrypoint.sh;
}
