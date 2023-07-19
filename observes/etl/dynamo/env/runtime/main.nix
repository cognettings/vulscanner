{
  __system__,
  inputs,
  makeTemplate,
  projectPath,
  ...
}: let
  pkg = (inputs.flakeAdapter {src = projectPath inputs.observesIndex.etl.dynamo.root;}).defaultNix;
  env = pkg.outputs.packages."${__system__}".env.runtime;
in
  makeTemplate {
    searchPaths = {
      bin = [env];
    };
    name = "observes-etl-dynamo-etl-conf-env-runtime";
  }
