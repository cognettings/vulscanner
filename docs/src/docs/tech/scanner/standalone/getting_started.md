---
id: getting_started
title: Getting started
sidebar_label: Getting started
slug: /tech/scanner/standalone/getting_started
---


We use [Makes](https://makes.fluidattacks.com/getting-started/)
to distribute our product,
therefore, we strongly recommend you to follow
the installation process that is described
in the official documentation page.

## Using Machine Standalone

1. Make sure you are in a Linux x86_64 system:

   ```sh
   $ uname -ms
   Linux x86_64
   ```

1. Now you can use Machine Standalone by calling:

   ```sh
   $ m gitlab:fluidattacks/universe@trunk /skims
   ```

   Usage:

   ```bash
   skims [OPTIONS] COMMAND [ARGS...]
   ```

   More info about the existent options [here](options/).

   You can run the scanner with:

   ```sh
    $ m gitlab:fluidattacks/universe@trunk /skims scan /path/to/config.yaml

    ... 🚀 !!
   ```

   The configuration format is explained in the
   [Configuration guidelines](configuration/).

## Using Machine Standalone as a container

1. Install the image with the following command:

   ```sh
   $ docker pull ghcr.io/fluidattacks/makes/<arch>:latest
   ```

   Where `<arch>` can either be `amd64` or `arm64`.
   For this example we will be using `amd64`:

   ```sh
   $ docker pull ghcr.io/fluidattacks/makes/amd64:latest
   ```

1. Start the container by calling:

   ```sh
   $ docker run -it ghcr.io/fluidattacks/makes/amd64 bash
   ```

1. Now you can use Machine Standalone like this:

   ```sh
   $ m gitlab:fluidattacks/universe@trunk /skims
   ```

   Feel free to pass the --help flag
   to learn more about the things it can do for you.

## Machine Standalone in your CI/CD

A Makes container can be found
in the [container registry](https://github.com/orgs/fluidattacks/packages?repo_name=makes).

You can use it
to run Machine Standalone
on any service that supports containers,
including most CI/CD providers.

Make sure you choose one of the images
that specify the architecture.

### GitHub Actions

```yaml
   # .github/workflows/dev.yml
   name: Makes CI
   on: [push, pull_request]
   jobs:
      machineStandalone:
         runs-on: ubuntu-latest
         steps:
            - uses: actions/checkout@f095bcc56b7c2baf48f3ac70d6d6782f4f553222
            - uses: docker://ghcr.io/fluidattacks/makes/amd64:23.06
            name: machineStandalone
            with:
               args: m gitlab:fluidattacks/universe@trunk /skims scan /path/config
```

### GitLab CI

```yaml
   # .gitlab-ci.yml
   /machineStandalone:
      image: ghcr.io/fluidattacks/makes/amd64:23.06
      script:
         - m gitlab:fluidattacks/universe@trunk /skims scan /path/config
```

### Travis CI

```yaml
   # .travis.yml
   os: linux
   language: nix
   nix: 2.3.12
   install: nix-env -if https://github.com/fluidattacks/makes/archive/23.06.tar.gz
   jobs:
      include:
         - script: m gitlab:fluidattacks/universe@trunk /skims scan /path/config
```
