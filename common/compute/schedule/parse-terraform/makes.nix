{outputs, ...}: {
  lintPython = {
    modules = {
      commonComputeScheduleParseTerraform = {
        python = "3.9";
        src = "/common/compute/schedule/parse-terraform/src";
        searchPaths = {
          source = [outputs."/common/utils/types_self"];
        };
      };
    };
  };
}
