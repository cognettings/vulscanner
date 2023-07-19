---
id: common
title: Common
sidebar_label: Common
slug: /tech/scanner/standalone/output/common
---

No matter what output format you choose,
the CLI will always display
some information before
and after the vulnerability reports.

## Before

```markup
[INFO] Official Documentation: https://docs.fluidattacks.com/machine/scanner/standalone/
[INFO] Namespace: namespace
[INFO] info HEAD is now at: 7d140e5fdba3bf3cefb4ba7b0d0ab139e1942152
[INFO] Startup work dir is: /any/universe
[INFO] Moving work dir to: /any/universe
[INFO] Files to be tested: 1
[INFO] Analyzing path 1 of 1: /test/data/lib_root/f052/java_cipher_jmqi.java
```

First,
Machine will provide the official documentation for the tool.
We strongly encourage end users to refer to this documentation in case
of any issues or questions.

After that,
the tool will display information about the current execution,
such as the namespace,
the commit being used,
the working directory,
and the total number of files to be scanned.

Finally,
for each target,
we will see a line indicating when the scan started for that target.

## After

```markup
[INFO] Summary: 1 vulnerabilities were found in your targets.
```

After the scan is completed,
Machine will provide a summary of the execution,
including the total number of vulnerabilities found.
If you chose CSV format,
this summary line will also appear
at the end of the result file.
