---
id: apk
title: Apk
sidebar_label: Apk
slug: /tech/scanner/standalone/configuration/apk
---

To activate the reversing checks
for Android APKs,
you need to use this key.
To ensure that it works correctly,
you must use the `include` key
to specify the path to the file
or folder that needs to be analyzed.

```yaml
namespace: namespace
apk:
  include:
    - /path/to/build/awesome-app-v1.0.apk
    - build/awesome-app-v1.0.apk
```

You can analyze multiple apk's
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
apk:
  include:
    - build/awesome-app-v1.0.apk
  exclude:
    - glob(src/**/test*.apk)
```
