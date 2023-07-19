{makeTemplate, ...}:
makeTemplate {
  name = "common-python-types";
  searchPaths = {
    pythonPackage = [./src];
  };
}
