---
id: reports
title: Download Reports
sidebar_label: Download Reports
slug: /tech/platform/analytics/reports
---

In the analytics section,
you can also download **reports.**
You have two options:
The
[download button,](/tech/platform/analytics/reports#download-button)
which you find in the three different analytics sections,
(Organization - Group and Portfolio)
and the
[Vulnerability report.](/tech/platform/analytics/reports#vulnerabilities-download)

## Download button

With this button you can  you can download the
charts and data from our three different Analytics sections.
To download the material of your interest,
you must go to one of the Analytics sections you are interested
in to download the information.
Here you will find the **Download button.**

![Download Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1664990254/docs/web/analytics/reports/download.png)

Clicking on this button
will download a `.png` file
that will provide you
with the complete information
we offer in that section.

![Information Report Example](https://res.cloudinary.com/fluid-attacks/image/upload/v1665510093/docs/web/analytics/reports/download_report.png)

## Vulnerabilities download

To download your organization's vulnerabilities
(including all vulnerability statuses) in a .CSV file,
go to the Analytics section at the Organization
level and click the Vulnerabilities button.

![Vulnerabilities report analytics](https://res.cloudinary.com/fluid-attacks/image/upload/v1682513649/docs/web/analytics/reports/vulnerabilities_report.png)

When you click on it,
you will be asked for a verification code that
will be sent to you via SMS.
If you have not yet registered your phone number to Fluid Attacks' platform,
we invite you to enter
[here](/tech/platform/user) and register.

![Vulnerabilities report sms](https://res.cloudinary.com/fluid-attacks/image/upload/v1682513910/docs/web/analytics/reports/sms.png)

When you enter the verification code,
you will download a compressed
file where you will find the
file with a .CSV extension.
When you open it,
you will be able to see all the
vulnerabilities of the organization.
You can also get this information
via API with the `vulnerabilitiesUrl` method.
To know how to make the API
request to our platform,
we invite you to click
[here](/tech/api).

> **Note:** Downloading this vulnerability report is
> only enabled for the [User Manager role.](/tech/platform/groups/roles#user-manager-role)
