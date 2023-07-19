---
id: dast
title: Dast
sidebar_label: Dast
slug: /tech/scanner/standalone/configuration/dast
---

With this key you activate
the Dynamic Application Security Testing (DAST)
for your endpoints or cloud environments.
To ensure that it works correctly,
you must use the `urls` key to specify
the target that needs to be analyzed.

```yaml
namespace: namespace
dast:
  urls:
    - https://localhost.com
    - https://localhost.com:443
```

Or if you are analyzing cloud environments
you should provide the credentials used
to access each one of them as follows:

```yaml
namespace: namespace
dast:
  aws_credentials:
    - access_key_id: "000f"
      secret_access_key: "000f"
    - access_key_id: "000e"
      secret_access_key: "000e"
```

You can analyze multiple targets
in an execution.

## Optional keys

### Lib_ssl and Lib_http

In our DAST component we have two submodules
called [ssl](/development/products/skims/guidelines/lib-module/dast#ssl)
and [http](/development/products/skims/guidelines/lib-module/dast#http).
If you want to disable
the reports for either of them,
you should do it in the following way:

```yaml
# In this example Machine will not report anything.
namespace: namespace
dast:
  urls:
    - http://localhost.com
  lib_ssl: false
  lib_http: false
```

These two keys expect a value either `false` or `true`
and by default they are set to true.
