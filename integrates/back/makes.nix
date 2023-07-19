{
  imports = [
    ./dev/makes.nix
    ./lint/makes.nix
    ./deploy/worker/makes.nix
  ];
  securePythonWithBandit = {
    integratesBack = {
      python = "3.11";
      target = "/integrates/back/src";
    };
  };
}
