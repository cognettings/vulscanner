{
  __system__,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  check = pkg.outputs.packages."${__system__}".check.types;
in
  makeTemplate {
    searchPaths = {
      bin = [check];
    };
    name = "observes-etl-dynamo-etl-conf-check-types";
  }
