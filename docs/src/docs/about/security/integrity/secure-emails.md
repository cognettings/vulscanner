---
id: secure-emails
title: Secure Emails
sidebar_label: Secure Emails
slug: /about/security/integrity/secure-emails
---

The [`Fluid Attacks` domain](https://fluidattacks.com/)
has DKIM and SPF protocols enabled.
Additionally,
it has the DMARCv1 protocol enabled
in verbose mode
for the running of advanced diagnostics.
These protocols help email recipients
verify if an email comes from a trusted source,
thus helping them avoid phishing
and fake emails.

## Requirements

- [115. Filter malicious emails](/criteria/requirements/115)
- [118. Inspect attachments](/criteria/requirements/118)
- [121. Guarantee uniqueness of emails](/criteria/requirements/121)
- [123. Restrict the reading of emails](/criteria/requirements/123)
