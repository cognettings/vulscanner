---
id: sast
title: Sast
sidebar_label: Sast
slug: /tech/scanner/standalone/configuration/sast
---

With this key you activate the Security Analysis and Static Testing (SAST)
for your source code. To ensure that it works correctly,
you must use the `include` key to specify the path(s) to the file(s)
or folder that needs to be analyzed.

```yaml
namespace: namespace
sast:
  include:
    - /path/to/file
    - /path/to/folder
```

You can analyze multiple paths in an execution.

:::tip
Read the [Format](../format) section for information about
the path format recognized by Machine.
:::

## Optional keys

### Exclude

If you are analyzing multiple files, you will probably want
to omit some contents. For that you can use
the exclude key to list the files or folders
you want to skip so that they are ignored at runtime.

```yaml
namespace: namespace
sast:
  include:
    - /path/to/folder
  exclude:
    - /path/to/folder/ignore_this_file.js
    - /path/to/folder/ignore_this_folder
```

### Lib_path and Lib_root

In our SAST component we have two
submodules called [path](/development/products/skims/guidelines/lib-module/sast#path)
and [root](/development/products/skims/guidelines/lib-module/sast#root).
If you want to disable the reports for either of them,
you should do it in the following way:

```yaml
# In this example Machine will not report anything.
namespace: namespace
sast:
  include:
    - /path/to/folder
  lib_path: false
  lib_root: false
```

These two keys expect a value either `false` or `true`
and by default they are set to true.

### Recursion Limit

In the [root](/development/products/skims/guidelines/lib-module/sast#root) module
we use an algorithm called Symbolic Evaluation, in order to search for
vulnerabilities in code files.

This uses several recursive functions which could lead to time out errors
when running the scanner. If you want to set a recursion limit to avoid this,
you can do it directly in the configuration, in the following way:

```yaml
# In this example Machine will not report anything.
namespace: namespace
sast:
  recursion_limit: 1000
  include:
    - .
  exclude: []
```

This key is optional, but must be set to a positive integer. We recommend an
initial value between 100-1000 in order to perform the first tests on a repo.
