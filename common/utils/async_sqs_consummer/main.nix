{
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "common-async-sqs-consummer";
  searchPaths = {
    pythonPackage = [./src];
    source = [outputs."/common/utils/types_self"];
  };
}
