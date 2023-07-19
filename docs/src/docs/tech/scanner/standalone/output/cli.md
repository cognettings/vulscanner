---
id: cli
title: CLI
sidebar_label: CLI
slug: /tech/scanner/standalone/output/cli
---

This is how the Machine Standalone output looks like
when it finds a vulnerability in your target:

```markup
[INFO] 052. Insecure encryption algorithm: namespace//any/test/data/lib_root/f052/java_cipher_jmqi.java

   1 | import com.ibm.mq.*;
   2 | import com.ibm.mq.jmqi.JmqiUtils;
   3 | import org.apache.log4j.Logger;
   4 |
   5 | class Test {
   6 |
   7 |  private final String cipherSuite = "TLS_RSA_WITH_AES_128_CBC_SHA256";
   8 |
   9 |  public void insecure() {
> 10 |   JmqiUtils.toCipherSuite(cipherSuite);
  11 |  }
  12 |
  13 |  public void secure() {
  14 |   String safeSuite = "TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256";
  15 |   JmqiUtils.toCipherSuite(safeSuite);
  16 |  }
  17 |
  18 | }
     ^ Col 0
CWE-310 - CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C
More information in: https://docs.fluidattacks.com/criteria/vulnerabilities/052
```

## Explanation

In the first line,
Machine will provide the title of
the [finding](/criteria/vulnerabilities) corresponding to
the detected vulnerability,
as well as its location,
which will be presented in the following format:

```markup
<namespace_of_execution>/<path_to_file>
```

After this information,
Machine will print a code snippet with a pointer `>`
indicating the exact line where the problem is.

```markup
   1 | import com.ibm.mq.*;
   2 | import com.ibm.mq.jmqi.JmqiUtils;
   3 | import org.apache.log4j.Logger;
   4 |
   5 | class Test {
   6 |
   7 |  private final String cipherSuite = "TLS_RSA_WITH_AES_128_CBC_SHA256";
   8 |
   9 |  public void insecure() {
> 10 |   JmqiUtils.toCipherSuite(cipherSuite);
  11 |  }
  12 |
  13 |  public void secure() {
  14 |   String safeSuite = "TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256";
  15 |   JmqiUtils.toCipherSuite(safeSuite);
  16 |  }
  17 |
  18 | }
     ^ Col 0
```

After the code snippet,
the output will display
the corresponding Common Weakness Enumeration (CWE)
and Common Vulnerability Scoring System (CVSS) vector for each report.
It is important to note
that a single finding could be associated
with multiple CWEs,
but only one CVSS is calculated for each one of them.
For example:

```markup
CWE-310 - CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C
```

Finally,
after each report,
a link to more information about
the particular vulnerability will be provided.
This may include examples of the vulnerability
and an estimate of how much time may be needed to remediate it.

```markup
More information in: https://docs.fluidattacks.com/criteria/vulnerabilities/052
```
