{outputs, ...}: {
  lintPython = {
    modules = {
      commonOktaParse = {
        python = "3.9";
        src = "/common/okta/parse/src";
        searchPaths = {
          source = [outputs."/common/utils/types_self"];
        };
      };
    };
  };
}
