---
id: extensive-logs
title: Extensive Logs
sidebar_label: Extensive Logs
slug: /about/security/non-repudiation/extensive-logs
---

Typical logs are also essential
for a non-repudiation policy to be successful.
Currently,
we store logs for:

- **Platform logging system:**
  [Our platform](https://app.fluidattacks.com/)
  stores a historical status of projects,
  findings, vulnerabilities,
  and other critical components.
  Changes made to these components are always tied
  to a user and a date.
  The historical status never expires.
  These logs cannot be modified.

- **Platform error tracking system:**
  Our platform provides real-time logging of errors
  that occur in its production environments.
  It is especially useful for quickly detecting
  new errors and hacking attempts.
  These logs never expire and cannot be modified.

- **Redundant data centers:**
  These store comprehensive logs of all
  our infrastructure components.
  Logs here never expire and cannot be modified.

- **DevSecOps execution:**
  Whenever a client's
  [CI pipeline](https://docs.fluidattacks.com/about/security/integrity/developing-integrity#continuous-integration)
  runs DevSecOps,
  logs containing information
  such as who ran it,
  vulnerability status,
  and other relevant data are uploaded
  to our data centers.
  This allows us to always know
  the current status of our client's DevSecOps service.
  These logs never expire and cannot be modified.

- **IAM authentication:**
  Our IAM stores logs of user login attempts,
  accessed applications,
  and possible threats.
  Logs here expire after seven days
  and cannot be modified.

- **Collaboration systems activity:**
  Our collaboration systems,
  such as email, calendar, etc.,
  store comprehensive talent activity logs,
  spam, phishing and malware emails,
  suspicious login attempts,
  and other potential threats.
  Talent activity logs never expire.
  Other security logs expire after 30 days.
  These logs cannot be modified.

- **CI job logs:**
  All our CI pipelines
  provide a full record of who triggered them,
  when,
  and the console output.
  These logs never expire and cannot be modified.

## Requirements

- [075. Record exceptional events in logs](/criteria/requirements/075)
- [079. Record exact occurrence time of events](/criteria/requirements/079)
- [080. Prevent log modification](/criteria/requirements/080)
- [376. Register severity level](/criteria/requirements/376)
- [377. Store logs based on valid regulation](/criteria/requirements/377)
