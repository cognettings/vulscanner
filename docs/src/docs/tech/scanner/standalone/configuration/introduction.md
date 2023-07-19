---
id: introduction
title: Introduction
sidebar_label: Introduction
slug: /tech/scanner/standalone/configuration
---

Skims uses a configuration file in [YAML](https://yaml.org/) syntax.

The general schema is shown and described below:

```yaml
namespace: repository
working_dir: /path/to/your/repository
commit: sha_of_the_commit of the scanner's source repo
language: EN
output:
  file_path: /path/to/results.csv
  format: CSV
checks:
  - F052
sast:
  include:
    - /path/to/file/or/dir
    - src/main/java/org/test/Test.java
    - glob(*)
    - glob(**.java)
    - glob(src/**/test*.py)
sca:
  include:
    - .
apk:
  include:
    - /path/to/build/awesome-app-v1.0.apk
    - build/awesome-app-v1.0.apk
dast:
  urls:
    - https://localhost.com
    - https://localhost.com:443
  ssl_checks: true
  http_checks: true
  aws_credentials:
    - access_key_id: "000f"
      secret_access_key: "000f"
debug: true
strict: false
```

## Configuration keys

The following is a detailed explanation of what each key in the configuration
file represents.

### namespace

An arbitrary name for the analysis. Normally the name of the repository
to be analyzed.

This is the only mandatory key for the configuration file. All the rest
are optional keys to be personalized for each analysis needs. There should
be no issues with the tool if any of them are not included in
the configuration file.

### working_dir

Used as the path to the repository.
With this key, the paths you configure in the dast and apk keys
could be relative paths to this directory.

### commit

Used to run Machine using a specific commit of its source repo.
For this you have to pass the commit sha of the version you want to use.
You can see the list of commits
[here](https://gitlab.com/fluidattacks/universe/-/commits/trunk?ref_type=heads)

### language

Language used to generate reports, valid values are: `EN`, `ES`.
If not present, defaults to EN (English).

### output

By default, the vulnerabilities that Machine finds in your code will appear
in the terminal. However, you can modify this configuring this key with the
two attributes:

- `file_path`: Defines where you want to store the output
- `format`: Defines the format of the output; valid values are `CSV` or `SARIF`

### checks

This configuration key specifies which findings are run.
Each finding represents a type of vulnerability.
The complete list of findings supported by machine can be found
[here](https://gitlab.com/fluidattacks/universe/-/blob/trunk/skims/manifests/findings.json)
and a detailed description of each finding can be found
[here](/criteria/vulnerabilities)

If the key is not present, all the findings supported by machine are run.
As a user, we recommend you not to use this key, to ensure your repo is checked
against ALL currently supported findings.

### apk, dast and sast

SAST refers to Static Application Security Testing, this enables the scanner
to check code files in any of the supported languages.

DAST refers to Dynamic Application Security Testing, this enables the scanner
to check vulnerabilities in dynamic environments (urls and cloud environments)

APK enables the scanner to perform reverse engineering in APK files to search
for vulnerabilities.

Each of these keys will be described thoroughly in its respective section.

- [sast](/tech/scanner/standalone/configuration/sast)
- [apk](/tech/scanner/standalone/configuration/apk)
- [dast](/tech/scanner/standalone/configuration/dast)

### debug

This key can be used to run the scanner under a debug mode.
Currently, this mode is only available for sast checks, and it enables the
scanner to generate two svg files in the ./skims folder of the home directory.

This is useful for developers, when adding sast checks.
As a user, it is not recommended that you run the scanner using this option.

For more details, please check the
[development docs](/development/products/skims/guidelines/lib-module/root.md)

### strict

With this option you can run the scanner in strict mode,
which means that it will fail the execution (with an exit code 1)
if it finds at least one vulnerability in your targets.

Ideal for using the scanner as a CI/CD job.
