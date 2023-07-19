---
id: faq
title: FAQ
sidebar_label: FAQ
slug: /about/faq
---

In this section,
we answer frequently asked questions
about our [platform](/tech/platform/introduction).

## Group

### What is a group?

Each [group](/tech/platform/groups/group-view/#group-table)
corresponds to individual projects our
clients create to manage their
[vulnerabilities](/tech/platform/groups/vulnerabilities/)
separately.
Inside a group on the
[platform](/tech/platform/introduction),
there are several sections that can be
accessed according to the
[role](/tech/platform/groups/roles/)
and plan you are subscribed to.
For more information on groups and sections,
please see our [Documentation.](/tech/platform/groups/introduction)

### Why do we advise you to create several groups?

It is recommended to create several
separate [groups](/tech/platform/groups/introduction),
each dedicated to one project;
you can have better visibility of
[vulnerabilities](/tech/platform/groups/vulnerabilities/)
for their management,
generate focused [reports](/tech/platform/groups/reports/)
and certificates independently,
have an organized view of the
[analytics](/tech/platform/analytics/),
and have a better track of the details of
each project you work on.

## Vulnerabilities

### What are vulnerabilities?

[Vulnerabilities](/criteria/vulnerabilities/)
are the noncompliance with cybersecurity
[requirements](/criteria/requirements/),
which are rules based on the several international
[standards](/criteria/compliance/)
we check in our comprehensive tests.

### What is the difference between Age and Last report in the Vulnerabilities table?

Age refers to how many days the
[vulnerability](/tech/platform/groups/vulnerabilities)
has been open,
whereas last report is the total number
of days passed since the vulnerability
was last reported.

### How do I suggest that a vulnerability is a false positive?

Choose Request [zero risk](/tech/platform/vulnerabilities/management/zero-risk/)
as its [treatment.](/tech/platform/vulnerabilities/management/treatments)

### How can I see only the findings of the dynamic application security testing (DAST)?

Find the [search bar](/tech/platform/groups/vulnerabilities#search-bar)
in the [Vulnerabilities table](/tech/platform/groups/vulnerabilities).
By entering **"HTTP"** as a keyword,
you will see the great majority of
vulnerabilities as **“dynamic” (found through DAST)**

### How can I see vulnerabilities specific to a particular Git root?

In the [search bar](/tech/platform/groups/vulnerabilities#search-bar)
that you can find in the
[Vulnerabilities table](/tech/platform/groups/vulnerabilities),
enter the nickname of the repository
you are interested in,
and the table will show you only the
vulnerabilities reported in that repository.

## Evidence

### How many pieces of evidence (images and videos) do I have access to?

There is a limit of six files
(images or videos).
However,
these are constantly updated according to
the reattacks or new vulnerabilities that
may be reported.

## Scope

### What is a nickname?

A nickname is how the team can identify a
[root](/tech/platform/groups/scope/roots/)
or set of
[credentials](/tech/platform/organization/tech/platform/organization/credentials/),
making it easier to search for or identify them.

### Where can I find my repository's nickname?

In the [Git root](/tech/platform/groups/scope/roots/#git-roots)
table in the [Scope](/tech/platform/groups/scope) section.

## Reattack

### How many hours do I have to wait for a response to a reattack request?

Up to 16 hours,
according to our
[service-level agreement](/plans/sla/response/).

### How to request a reattack?

A [reattack](/tech/platform/reattacks/)
can be requested from the
[Locations](/tech/platform/vulnerabilities/management/locations/#reattack)
and
[To-do list](/tech/platform/vulnerabilities/management/to-do)
section.
You must select the vulnerability to
attack followed by clicking the
**Reattack** button.
Then,
the selected vulnerability will show
the status **Requested** in the
**Reattack** column for up to 16 hours.
Remember to check the
[Consulting](/tech/platform/support/consulting/#concerning-vulnerabilities)
section for any new comments regarding the reattack.

### How do I know that a requested reattack is in progress?

You can check the reattack status in
the column called **Reattack** in the
[Locations](/tech/platform/vulnerabilities/management/locations/#locations-table)
section.
You can also check in the
[Consulting](/tech/platform/support/consulting/#concerning-vulnerabilities)
whether there are comments  on the request.

## Certificate

### How do I generate a service certificate?

In the [Vulnerabilities](/tech/platform/groups/vulnerabilities/)
section,
click on the [Generate report](/tech/platform/groups/reports/)
button and select the **Certificate**
option.
However,
this option will not be available if
you have not filled out the
**Business Registration Number**
and **Business Name** fields in the
[Information](/tech/platform/groups/scope/other-sections/information)
section.
Remember that the roles that can download
certifications are
[user manager](/tech/platform/groups/roles/#user-manager-role)
and [vulnerability manager](/tech/platform/groups/roles/#vulnerability-manager-role).

## Reports

### How do I generate the vulnerability report?

In the [Vulnerability](/tech/platform/groups/vulnerabilities/)
section,
click the [Generate report](/tech/platform/groups/reports/)
button and select which type of
[report](/tech/platform/groups/reports/)
you want to download,
either **technical** or **executive**.
Remember that you must register your
[mobile number](/tech/platform/user/)
beforehand to enable two-factor authentication
to download the report.
Remember that the roles that can download
reports are [user manager](/tech/platform/groups/roles/#user-manager-role)
and [vulnerability manager](/tech/platform/groups/roles/#vulnerability-manager-role).

### What is the difference between executive and technical reports?

The **executive report** is a summary
report in PDF format,
generally intended for personnel in
management roles.
This report contains concise and clear
information on the vulnerabilities
reported in the group.
On the other hand,
the **technical report** is an XLSX file
where you have all the vulnerabilities
reported in the group with their technical details.

## Members

### What is the difference between members and authors?

[Members](/tech/platform/groups/members)
refers to  all users who can access
your group to visualize information
or manage vulnerabilities,
scope and tags,
among other things.
[Authors](/tech/platform/groups/members)
are all the developers or professionals who
contribute to the repositories under evaluation.

## Consulting

### What is the difference between our three consulting alternatives?

[Consulting](/tech/platform/support/consulting/)
is one of the communication channels with users.
You can find it in
Locations,
Groups and Events.
Use the one in
[Locations](/tech/platform/support/consulting/#concerning-vulnerabilities)
when you have questions regarding
a specific vulnerability.
Use the one in
[Events](/tech/platform/support/consulting#concerning-events)
to ask about the status or details of
situations that are preventing security
testing from resuming.
And use the one in the main screen of a
[group](/tech/platform/support/consulting#concerning-groups)
to ask general questions about that group.

## Treatments

### Why is a vulnerability still Vulnerable when it has been accepted permanently?

When a vulnerability is permanently accepted,
the organization assumes the risk,
not remediating it,
so it will continue to be regarded as vulnerable.

### What happens when a temporary acceptance treatment expires?

The treatment for that specific security
issue reverts back to **Untreated**,
and the remediation of such issue is assigned
to the user who had requested the temporary acceptance.

## Policies

### If I apply policies to a group, will these apply to all roots of this?

Yes,
it will apply to all repositories added in that group.

### What is the difference between policy at the ORG and the group level?

[Organization policies](/tech/platform/organization/policies)
are those that you set globally and
that will be inherited by all groups
pertaining to that organization.
For your management purposes,
you may prefer to set specific
[group policies](/tech/platform/groups/scope/other-sections/policies).

## Agent

### Must I only install Docker to run the DevSecOps agent from my local machine?

Yes,
it is only necessary to use Docker if
you manage the DevSecOps agent from your
local machine.
To see the Docker and agent installation
steps visit our
[Documentation](/tech/ci/installation/).

### Does Fluid Attacks’ DevSecOps agent run locally or on the development infrastructure?

You can run it both ways.

### How many arguments can I pass to run Fluid Attacks’ DevSecOps agent?

You can pass multiple arguments.
To see the different options,
check out our
[Documentation](/tech/ci/installation/#options).

### How often is it advisable to do docker pull to update the image?

It is up to the user to do it weekly or monthly.

### In what mode can Fluid Attacks’ agent be run so it doesn't break the build?

In [lax mode](/tech/ci/installation/#arguments-to-run-your-agent),
opposite to strict mode.

### Must all team members use the same token to run the DevSecOps agent in a    group?

Yes,
all team members who want to run
the agent in the same group
require the same token.
To acquire the token,
you must go to the
[DevSecOps Agent](/tech/platform/groups/scope/other-sections/agent)
section in
[Scope](/tech/platform/groups/scope/roots/).

## API

### How can I start using the platform API?

To begin using the API,
we recommend you read our step-by-step guide
in our [Documentation](/tech/api).
Bear in mind that to make requests to the
API you will need prior knowledge of the
GraphQL language.

## Platform problems

If you have any problems logging in
to the platform,
we recommend the following:

- Log out of the platform,
  delete browser cache and cookies,
  log back in,
  and enter the group(s) with the inconvenience.

- Try to access the platform from incognito mode
  or another browser and check if the problem also occurs.

- Once the screenshot is displayed,
  you can also run one of the following JS commands
  from the browser's development console
  (usually accessed by pressing F12 in Windows and Linux environments):
  sessionStorage.clear() or localStorage.clear()
  and then refresh the web page.
