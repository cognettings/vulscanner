---
id: encryption-transit
title: Encryption in Transit
sidebar_label: Encryption in Transit
slug: /about/security/confidentiality/encryption-transit
---

All our applications and services have industry-standard
[encryption in transit](/criteria/requirements/224).

- The [`Fluid Attacks`](https://fluidattacks.com/) domain
  uses the latest [TLSv1.3](/criteria/requirements/181)
  cryptographic protocol
  for maximum protection of data in transit.

- We maintain an SSL A+ score from
  [SSL Labs](https://www.ssllabs.com/ssltest/analyze.html?d=fluidattacks.com&latest).

- Digital certificates for `Fluid Attacks` are renewed
  every 30 days
  in order to minimize leaks.

- We use the
  [HSTS](https://es.wikipedia.org/wiki/HTTP_Strict_Transport_Security)
  policy
  to ensure that every connection to our domain
  goes through [HTTPS](https://en.wikipedia.org/wiki/HTTPS).

- We demand all connections
  to support at least TLSv1.2.

- [Our platform's](https://app.fluidattacks.com/)
  database uses TLSv1.2
  for the protection of data in transit.

- We possess fully dedicated network channels
  with some of our biggest clients,
  allowing us to isolate all unwanted traffic.
  This is particularly useful
  for running secure dynamic application hacking.

- For the rest of our clients,
  we use fully encrypted VPNs.

- [Ephemeral environments](../integrity/developing-integrity#ephemeral-environments)
  always include a digital certificate,
  validated with ACME protocol,
  and [not self-signed](/criteria/requirements/092).

## Requirements

- [092. Use externally signed certificates](/criteria/requirements/092)
- [147. Use pre-existent mechanisms](/criteria/requirements/147)
- [181. Transmit data using secure protocols](/criteria/requirements/181)
- [336. Disable insecure TLS versions](/criteria/requirements/336)
