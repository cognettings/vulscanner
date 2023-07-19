{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "integrates-back-lint-asyncdef";
  replace.__argIntegratesBackEnv__ = outputs."/integrates/back/env";
}
