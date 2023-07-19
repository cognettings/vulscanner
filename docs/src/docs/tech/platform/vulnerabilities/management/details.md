---
id: details
title: Vulnerability details
sidebar_label: Vulnerability details
slug: /tech/platform/vulnerabilities/management/details
---

It is helpful for you to learn
the most relevant information
about the vulnerabilities
reported in your system.
This information includes
vulnerability status,
display of vulnerable code,
defined treatments and
tracking history.
We provide this information in
the **Vulnerability** pop-up
window that appears when you
click on any vulnerability in
the
[**Locations**](/tech/platform/vulnerabilities/management/locations/)
tab or the
[**To do**](/tech/platform/vulnerabilities/management/to-do)
section.
This window has five tabs:
**Details**,
**Severity**,
**Code**,
**Treatments**
and **Tracking**.

## Details tab

In the **Details** tab,
you can see the vulnerability’s
status –whether it is open or
closed–, location,
last reattack request date
and current treatment.

![Vulnerability Detail Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1674000974/docs/web/vulnerabilities/management/detailstab.png)

Here we explain the information of each item:

- **Location**:
  - **Locations**:
    Path where the vulnerability was found.
  - **LoC / Port / Input**:
    The location specified is either the code line,
    port number,
    or input field.
- **General details**:
  - **Report date**:
    Date vulnerability reported.
  - **Closing date**:
    The date vulnerability was closed.
  - **Commit hash**:
    Commit ID where the vulnerability was found.
  - **Tags**:
    Vulnerability identification tags.
  - **Level**:
    The user's rating of the vulnerability
    indicates how important/critical it is.
  - **Technique:**
    Security technique used to identify this specific location.
- **Reattacks**:
  - **Last request**:
    Date of last time a re-attack was requested.
  - **Requester**:
    The name of the person requesting the reattack.
  - **Cycles**:
    Total of how many reattacks have been requested.
  - **Efficiency**:
    Percentage of efficiency in the solution
    of vulnerabilities.
- **Treatments**:
  - **Current**:
    Current treatment of vulnerability.
  - **Assigned**:
    The person assigned the vulnerability.
  - **Date**:
    Date stipulated in the application
    of the treatment.
  - **Expiration**:
    Date stipulated in the application of
    the treatment Temporarily Accepted.
  - **Justification**:
    The justification given when
    Temporarily Accepted treatment was applied.
  - **Changes**:
    The number of times the treatment of
    that vulnerability has changed.

## Severity tab

In the Severity tab,
you will find expanded information about the
severity score of that specific location.
Here you are presented with the related
**Vector string**, the calculated numerical
severity score and a visual representation
where you can hover over each metric to obtain
greater detail.

![Severity Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1687990469/docs/web/vulnerabilities/management/severity_tab_details.png)

If you want to know more about the
fields of this score,
click [here](/talent/hacking/analysts/new-vuln-severity).

There is also a link in the given **Vector string**,
where you are redirected to the
[CVSS v3.1 calculator][CVSS_CALCULATOR]
and get the assigned severity score,
allowing you to understand this better.

## Code tab

Next to details tab is code
is **Code** tab.
Here you can see the vulnerable
portion of the code,
being this a clear reference
where the vulnerability is pointed
out directly from the code.

![Code Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1668514617/docs/web/vulnerabilities/management/code_tab.png)

> **Note:** This tab is exclusive only,
> to vulnerability type SAST.

## Treatments tab

In the **Treatments** tab,
you can modify the vulnerability’s
defined treatment.
If you would like to know more
about the treatments you can
define for a vulnerability,
follow
[this link](/tech/platform/vulnerabilities/management/treatments).

![Treatments Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1668515370/docs/web/vulnerabilities/management/treatments_Tab.png)

## Tracking tab

Lastly,
in the **Tracking** tab,
you can learn how the
vulnerability has evolved
over time.
Find out more information about
this tab under
[this link](/tech/platform/vulnerabilities/management/tracking).

![Tracking Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1674001175/docs/web/vulnerabilities/management/tracking_tab.png)

[CVSS_CALCULATOR]: https://www.first.org/cvss/calculator/3.1
