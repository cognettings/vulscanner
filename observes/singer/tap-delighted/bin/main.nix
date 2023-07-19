{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    import_and_run tap_delighted.cli main "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/common/import-and-run"
      outputs."${inputs.observesIndex.tap.delighted.env.runtime}"
    ];
  };
  name = "observes-singer-tap-delighted-bin";
}
