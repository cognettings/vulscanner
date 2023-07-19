{outputs, ...}: {
  lintPython = {
    modules = {
      melts = {
        searchPaths.source = [
          outputs."/melts/config/development"
          outputs."/melts/config/runtime"
          outputs."/melts/config/type-stubs"
        ];
        python = "3.11";
        src = "/melts/src";
      };
    };
  };
}
