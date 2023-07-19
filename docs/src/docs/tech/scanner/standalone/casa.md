---
id: casa
title: CASA
sidebar_label: CASA
slug: /tech/scanner/standalone/casa
---

If your goal is to use Machine Standalone
to scan your application
and thereby meet the Tier 2 requirements of CASA,
you should take the following into account:
As of today,
[AppDefenseAlliance's documentation](https://appdefensealliance.dev/casa/tier-2/ast-guide/static-scan)
on our tool is outdated.
For that reason,
on this page,
we are going to help you correct the problems
so that you can successfully complete your scan.

## Configuration file

As you may know,
our tool uses a YAML file to configure the scan.
AppDefenseAlliance recommends a YAML file that isn't entirely correct,
it's just that the `path` key has been renamed.
So, you should use the `sast` key instead.

Here is the updated YAML:

```yaml
namespace: OWASP
output:
  file_path: ./Fluid-Attacks-Results.csv
  format: CSV
working_dir: .
sast:
  include:
    - .
sca:
  include:
    - .
# Note: uncomment this if you want to analyze .apk files.
# apk:
  # include:
    #- /app/app-arm-debug-Android5.apk
    #- /app/app-arm-debug.apk
checks:
- F001
- F004
- F008
- F009
- F010
- F011
- F012
- F015
- F016
- F017
- F020
- F021
- F022
- F023
- F031
- F034
- F035
- F037
- F042
- F043
- F052
- F055
- F056
- F058
- F073
- F075
- F079
- F080
- F082
- F085
- F086
- F089
- F091
- F092
- F094
- F096
- F098
- F099
- F100
- F103
- F107
- F112
- F120
- F127
- F128
- F129
- F130
- F131
- F132
- F133
- F134
- F143
- F160
- F176
- F177
- F182
- F200
- F203
- F206
- F207
- F211
- F234
- F239
- F246
- F247
- F250
- F252
- F256
- F257
- F258
- F259
- F266
- F267
- F268
- F277
- F281
- F300
- F313
- F320
- F325
- F333
- F335
- F338
- F346
- F363
- F372
- F380
- F381
- F393
- F394
- F396
- F398
- F400
- F401
- F402
- F406
- F407
- F408
- F409
- F411
- F412
- F413
- F414
- F416
- F418
language: EN
```

More information about the configuration keys [here](configuration/)

## Running the scan

It is not necessary to create a Dockerfile to use the tool,
you only need to download the image.

```sh
$ docker pull ghcr.io/fluidattacks/makes/<arch>:latest
```

Where `<arch>` can either be `amd64` or `arm64`.
For this example we will be using `amd64`:

```sh
$ docker pull ghcr.io/fluidattacks/makes/amd64:latest
```

Now what you need to do is create
a local folder where you're going
to place the `config.yaml` file
and the folder or files you want to scan.

After that,
you have to run the following command to execute the scan,
and if everything goes well,
the .csv file with the scan results should be in
the local folder you created.

```sh
$ docker run -v <path_to_local_folder>:/working-dir ghcr.io/fluidattacks/makes/amd64 m gitlab:fluidattacks/universe@trunk /skims scan ./config.yaml
```
