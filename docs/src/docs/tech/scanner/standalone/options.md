---
id: options
title: Options
sidebar_label: Options
slug: /tech/scanner/standalone/options
---

Machine Standalone has three different options.

## --help

Feel free to pass the --help flag
to learn more about the things it can do for you.

This will provide you with information on how to use the tool,
as well as a short description of each existing flag.

Example:

```sh
$ m gitlab:fluidattacks/universe@trunk /skims --help
```

## --strict

With this option you can run Machine in strict mode,
which means that it will fail the execution (with an exit code 1)
if it finds at least one vulnerability in your targets.

Ideal for using Machine Standalone as a CI/CD job.

Example:

```sh
$ m gitlab:fluidattacks/universe@trunk /skims --strict scan path/to/config.yaml
```
