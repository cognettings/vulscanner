{
  makeSearchPaths,
  makeTemplate,
  outputs,
  ...
}: {
  dev = {
    integratesStreams = {
      source = [
        outputs."/integrates/streams/runtime"
        (makeSearchPaths {
          pythonPackage = [
            "$PWD/integrates/streams/src"
          ];
        })
      ];
    };
  };
}
