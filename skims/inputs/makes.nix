{
  fetchGithub,
  fromJsonFile,
  inputs,
  projectPath,
  ...
}: {
  inputs = {
    skimsAndroguard = fetchGithub {
      owner = "androguard";
      repo = "androguard";
      rev = "8d091cbb309c0c50bf239f805cc1e0931b8dcddc";
      sha256 = "sSNs51JvBAAEUmMY84wlmuB0nVdIyc+sBTFjr1nZl7g=";
    };
    skimsBenchmarkOwasp = fetchGithub {
      owner = "OWASP-Benchmark";
      repo = "BenchmarkJava";
      rev = "53732be42f3e780fd98d40b32f538062b3b19da9";
      sha256 = "0frrvrl4nyy8rllcpvgxazv9ybv61z49knhd6k0pmnasz2a53zga";
    };
    skimsNistTestSuites = fetchGithub {
      owner = "fluidattacks";
      repo = "NIST-SARD-Test-Suites";
      rev = "7189c65ab6e398180e3f2aa2de683466b4412821";
      sha256 = "CDLX3Xa7nCmzdJdAjlSzdlFIaUx3cg7GPiqc5c8Dj6Q=";
    };
    skimsVulnerableApp = fetchGithub {
      owner = "SasanLabs";
      repo = "VulnerableApp";
      rev = "f5334e84faadbfb4beec42849a2e8acc5e37a276";
      sha256 = "gVY9VPo0+2xHdbME61MH/JaMP8pyqWh5k7im3O8hNAc=";
    };
    skimsVulnerableJsApp = fetchGithub {
      owner = "fluidattacks";
      repo = "vulnerable_js_app";
      rev = "1282fbde196abb5a77235ba4dd5a64f46dac6e52";
      sha256 = "0sc6zx9zf2v5m2a0hfccynyn93mcx97ks6ksdf9larha6l5r977f";
    };
    skimsTestPythonCategories =
      fromJsonFile
      (projectPath "/skims/test/test_groups.json");
    skimsTestPythonCategoriesCI =
      builtins.filter
      (category: category != "_" && category != "all")
      inputs.skimsTestPythonCategories;
    skimsTreeSitterCSharp = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-c-sharp";
      rev = "7a47daeaf0d410dd1a91c97b274bb7276dd96605";
      sha256 = "1GRKI+/eh7ESlX24qA+A5rSdC1lUXACiBOUlgktcMlI=";
    };
    skimsTreeSitterDart = fetchGithub {
      owner = "fluidattacks";
      repo = "tree-sitter-dart";
      rev = "53485a8f301254e19c518aa20c80f1bcf7cf5c62";
      sha256 = "sha256-1IcvFcxIkcrOuq6bypD08PeYw6J/pL/MbYPt+dKHQbc=";
    };
    skimsTreeSitterGo = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-go";
      rev = "64457ea6b73ef5422ed1687178d4545c3e91334a";
      sha256 = "sha256-38pkqR9iEIEf9r3IHJPIYgKfWBlb9aQWi1kij04Vo5k=";
    };
    skimsTreeSitterHcl = fetchGithub {
      owner = "fluidattacks";
      repo = "tree-sitter-hcl";
      rev = "becebebd3509c02e871c99be55556269be1def1b";
      sha256 = "GR2a+VuhZVMGmLW9Mg7bSALNsy0SyfG+YVaRz1qY6a0=";
    };
    skimsTreeSitterJava = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-java";
      rev = "2efe37f92d2e6aeb25186e9da07455bb4a30163c";
      sha256 = "09v3xg1356ghc2n0yi8iqkp80lbkav0jpfgz8iz2j1sl7ihbvkyw";
    };
    skimsTreeSitterJavaScript = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-javascript";
      rev = "5720b249490b3c17245ba772f6be4a43edb4e3b7";
      sha256 = "sha256-rSkLSXdthOS9wzXsC8D1Z1P0vmOT+APzeesvlN7ta6U=";
    };
    skimsTreeSitterJson = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-json";
      rev = "73076754005a460947cafe8e03a8cf5fa4fa2938";
      sha256 = "wbE7CQ6l1wlhJdAoDVAj1QzyvlYnevbrlVCO0TMU7to=";
    };
    skimsTreeSitterKotlin = fetchGithub {
      owner = "fluidattacks";
      repo = "tree-sitter-kotlin";
      rev = "d5a5f91a017963f18bdf36fd75ef8bfeb8bbef4f";
      sha256 = "sha256-+TLeB6S5MwbbxPZSvDasxAfTPV3YyjtR0pUTlFkdphc=";
    };
    skimsTreeSitterPhp = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-php";
      rev = "1a40581b7a899201d7c2b4684ee34490bc306bd6";
      sha256 = "sha256-tSgCGV1w3gbt9Loar3+Auo2r7hqZwB7X+/g9Dfatp8I=";
    };
    skimsTreeSitterPython = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-python";
      rev = "62827156d01c74dc1538266344e788da74536b8a";
      sha256 = "sha256-hVtX4Dyqrq+cSvKTmKMxLbAplcCdR8dfFDoIZNtPFA0=";
    };
    skimsTreeSitterRuby = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-ruby";
      rev = "fe6a2d634da0e16b11b5aa255cc3df568a4572fd";
      sha256 = "sha256-e6D4baG3+paNUwyu5bMYESKUEzTnmMU4AEOvjEQicFQ=";
    };
    skimsTreeSitterScala = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-scala";
      rev = "918f0fb948405181707a1772cab639f2d278d384";
      sha256 = "sha256-/nPCajhhLTxFjRpnSRXSEGmFysyMKBAZN+Xtm6npzDk=";
    };
    skimsTreeSitterSwift = fetchGithub {
      owner = "fluidattacks";
      repo = "tree-sitter-swift";
      rev = "462813c6c589e5ffc859d4ed43dbd2ba6cba8013";
      sha256 = "ZKoYlzcntlHXED1pSSxYL7rQPG0b4mp/3ulbQ0457hE=";
    };
    skimsTreeSitterTsx = fetchGithub {
      owner = "tree-sitter";
      repo = "tree-sitter-typescript";
      rev = "b66d19b9b6ec3edf3d8aff0c20646acbdaa0afb3";
      sha256 = "sha256-YJrjxU2VmkVHTHta531fsJrx+K4Xih5kpFVEEqmvz34=";
    };
    skimsTreeSitterYaml = fetchGithub {
      owner = "fluidattacks";
      repo = "tree-sitter-yaml";
      rev = "32ac609651506657a54da01a0290193dfb8b9cc8";
      sha256 = "HmUmUPXGBXmpGg3qGaKuc9CvU1UfBYL8Xe1EUAXw4iI=";
    };
  };
}
