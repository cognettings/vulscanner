---
id: accuracy
title: Accuracy
sidebar_label: Accuracy
slug: /plans/sla/accuracy
---

## Description

**90%** of the severity of vulnerabilities is detected
and has some level of risk.

## Criteria

All of the following are necessary conditions
for the application of the service-level agreements:

- The group has a Squad Plan.
- Both the environment
  and the source code
  are accessible.
- The environment is paired with the code,
  i.e.,
  the environment corresponds to the provided branch.
- Stable environment
  (**80%** of business days
  with no open eventualities).
- Complete dataset
  for the corresponding use case.
- Remote access with no human intervention
  (no captcha, OTP, etc.).
- 100% Health Check was performed
  on a group potentially affected
  by a false negative.
- Average of **400** weekly changes per author
  from the start of service
  to the potential false negative report.

## Details

Besides the [general measurement aspects](/plans/sla/accuracy#details),
this SLA is measured
taking into account the following:

- The severity of vulnerabilities are calculated
  using CVSSF = 4^(CVSS-4).
- The accuracy is calculated
  based on the false positives,
  false negatives
  and the [F-Score model](https://en.wikipedia.org/wiki/F-score).
- Black vulnerabilities
  detectable only via source code
  are not considered false negatives.

## Indicator calculation

- Compute CVSSF for each location
  (CVSSF = 4 ^ (4 - CVSS))
- Distribute the total CVSSF
  between True Positives,
  False Positives and False Negatives.
- Compute intermediate indicators:

  - **Precision:**
    True Positives / (True Positives + False Positives)
  - **Recall:**
    True Positives / (True Positives + False Negatives)

- Compute the SLA as:
  2 x (Precision x Recall) / (Precision + Recall)
