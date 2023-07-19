{outputs, ...}: {
  lintPython = {
    modules = {
      commonAsynsSqsConsummer = {
        searchPaths.source = [
          outputs."/common/utils/async_sqs_consummer/env/pypi/runtime"
          outputs."/common/utils/async_sqs_consummer/env/pypi/type-stubs"
          outputs."/common/utils/types_self"
        ];
        python = "3.11";
        src = "/common/utils/async_sqs_consummer/src/async_sqs_consumer";
      };
    };
  };
}
