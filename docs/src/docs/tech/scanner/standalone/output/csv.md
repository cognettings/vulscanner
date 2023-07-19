---
id: csv
title: CSV
sidebar_label: CSV
slug: /tech/scanner/standalone/output/csv
---

This is how the Machine Standalone output looks like
when it finds a vulnerability in your target:

|title                             |cwe    |description                                                                                                             |cvss                                                      |finding                                                     |stream|kind |where                                                                           |snippet|method                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|----------------------------------|-------|------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|------------------------------------------------------------|------|-----|--------------------------------------------------------------------------------|-------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|052. Insecure encryption algorithm|CWE-310|Use of insecure encryption algorithm in namespace//home/any/universe/skims/test/data/lib_root/f052/java_cipher_jmqi.java|CVSS:3.1/AV:A/AC:H/PR:N/UI:N/S:U/C:L/I:N/A:N/E:F/RL:O/RC:C|https://docs.fluidattacks.com  /criteria/vulnerabilities/052|skims |SAST|10                                                                              |    1  import com.ibm.mq.*;    2  import com.ibm.mq.jmqi.JmqiUtils;    3  import org.apache.log4j.Logger;    4     5  class Test {    6     7   private final String cipherSuite = "TLS_RSA_WITH_AES_128_CBC_SHA256";    8     9   public void insecure() { > 10    JmqiUtils.toCipherSuite(cipherSuite);   11   }   12    13   public void secure() {   14    String safeSuite = "TLS_ECDHE_ECDSA_WITH_ARIA_128_GCM_SHA256";   15    JmqiUtils.toCipherSuite(safeSuite);   16   }   17    18  }      ^ Col 0 |java.java_insecure_cipher_jmqi

:::note
The CSV format is useful if you want to save your results for future reference,
or if you want to store them in an organized manner.
:::

This format will provide you
with the same information as the CLI output,
but it will be more specific
and provide additional details about
what has been found and how it was found.

For example,
the CSV format includes a description
and a categorization based on how
and where the vulnerability was found.

Finally,
in the last column,
you will find the name of
the method responsible for reporting
that specific vulnerability.
This will come in handy
if you want to create
an issue stating
that you found a false positive
in your Machine execution.
