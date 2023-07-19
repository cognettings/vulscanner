{
  inputs,
  makeSearchPaths,
  managePorts,
  ...
}:
makeSearchPaths {
  bin = [
    inputs.nixpkgs.python311Packages.flask
  ];
  source = [
    managePorts
  ];
  pythonPackage = [
    inputs.nixpkgs.python311Packages.flask
  ];
}
