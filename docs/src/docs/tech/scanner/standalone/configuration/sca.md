---
id: sca
title: SCA
sidebar_label: SCA
slug: /tech/scanner/standalone/configuration/sca
---

With this key you activate the Software Composition Analysis (SCA)
for your source code. To ensure that it works correctly,
you must use the `include` key to specify the path(s) to the file(s)
or folder that needs to be analyzed.

```yaml
namespace: namespace
sca:
  include:
    - /path/to/code/
    - /path/to/specific/package.json
```

You can analyze multiple files
in an execution.

:::tip
Read the [Format](../format) section for information about
the path format recognized by Machine.
:::

## Optional keys

### Exclude

If you are analyzing multiple files,
you will probably want to
omit some contents.
For that you can use
the exclude key to list
the files or folders
you want to skip
so that they are ignored at runtime.

```yaml
namespace: namespace
sca:
  include:
    - path/to/src/
  exclude:
    - glob(src/**/test*.json)
```
