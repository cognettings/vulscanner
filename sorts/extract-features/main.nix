{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "sorts-extract-features";
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/git"
      outputs."/common/utils/sops"
      outputs."/common/utils/common"
      outputs."/melts/lib"
      outputs."/observes/common/list-groups"
      outputs."/sorts/config/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
