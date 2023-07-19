---
id: new-vuln-severity
title: Severity score
sidebar_label: Severity score
slug: /talent/hacking/analysts/new-vuln-severity
---

This is the score that we give
to each vulnerability
in order to properly categorize
the risk that each of them
represent for the system.
To assign the correct score
to the vulnerability
we use the CVSS v3.1 standard
which has several metrics
by which to assign a score.
These are the mentioned metrics:

![Severity Metrics](https://res.cloudinary.com/fluid-attacks/image/upload/v1669232374/docs/web/vulnerabilities/new-vulnerability-types/new-vuln-severity/severity_score.png)

- **Attack Vector:**
  This metric reflects the context
  by which vulnerability exploitation
  is possible.
  This metric value
  (and consequently the Base Score)
  will be larger
  the more remote
  (logically, and physically)
  an attacker can be
  in order to exploit
  the vulnerable component.

- **Attack Complexity:**
  This metric describes the conditions
  beyond the attacker’s control
  that must exist
  in order to exploit the vulnerability.
  As described below,
  such conditions may require
  the collection of more information
  about the target,
  or computational exceptions.
  Importantly,
  the assessment of this metric
  excludes any requirements
  for user interaction
  in order to exploit the vulnerability
  (such conditions are captured
  in the User Interaction metric).

- **User Interaction:**
  This metric captures the requirement
  for a human user,
  other than the attacker,
  to participate
  in the successful compromise
  of the vulnerable component.
  This metric determines
  whether the vulnerability
  can be exploited
  solely at the will of the attacker,
  or whether a separate user
  (or user-initiated process)
  must participate in some manner.

- **Scope:**
  The Scope metric captures
  whether a vulnerability
  in one vulnerable component
  impacts resources in components
  beyond its security scope.
  The security scope of a component
  encompasses other components
  that provide functionality
  solely to that component,
  even if these other components
  have their own security authority.

- **Confidentiality Impact:**
  This metric measures the impact
  to the confidentiality
  of the information resources
  managed by a software component
  due to a successfully exploited
  vulnerability.
  Confidentiality refers to
  limiting information access
  and disclosure
  to only authorized users,
  as well as preventing access by,
  or disclosure to,
  unauthorized ones.

- **Integrity Impact:**
  This metric measures the impact to integrity
  of a successfully exploited vulnerability.
  Integrity refers to the trustworthiness
  and veracity of information.

- **Availability Impact:**
  This metric measures the impact
  to the availability
  of the impacted component
  resulting from a successfully
  exploited vulnerability.
  While the Confidentiality
  and Integrity impact metrics
  apply to the loss of confidentiality
  or integrity of data
  (e.g., information, files)
  used by the impacted component,
  this metric refers to
  the loss of availability
  f the impacted component itself,
  such as a networked service
  (e.g., web, database, email).
  Since availability refers to
  the accessibility of information resources,
  attacks that consume network bandwidth,
  processor cycles,
  or disk space
  all impact the availability
  of an impacted component.

- **Exploitability:**
  This metric measures the likelihood
  of the vulnerability being attacked,
  and is typically based on
  the current state of exploit techniques,
  exploit code availability,
  or active, “in-the-wild” exploitation.
  Public availability of easy-to-use exploit code
  increases the number of potential attackers
  by including those who are unskilled,
  thereby increasing the severity of the vulnerability.

- **Remediation Level:**
  The Remediation Level of a vulnerability
  is an important factor for prioritization.
  The typical vulnerability is unpatched
  when initially published.
  Workarounds or hotfixes
  may offer interim remediation
  until an official patch
  or upgrade is issued.

- **Report Confidence:**
  This metric measures
  the degree of confidence
  in the existence of the vulnerability
  and the credibility
  of the known technical details.
  Sometimes
  only the existence of vulnerabilities is publicized,
  but without specific details.
  For example,
  an impact may be recognized as undesirable,
  but the root cause may not be known.
  The vulnerability may later be corroborated by research
  which suggests where the vulnerability may lie,
  though the research may not be certain.
  Finally,
  a vulnerability may be confirmed
  through acknowledgment by the author
  or vendor of the affected technology.

- **Privileges Required:**
  This metric describes
  the level of privileges
  an attacker must possess
  before successfully exploiting the vulnerability.
  The Base Score is greatest
  if no privileges are required.

In order to check each of these metrics
in much more detail,
learn about all the possible values
that you can give them
and what they mean,
and also learn about the process
that produces the final score,
you can visit the official web page
that describes the CVSS v3.1 standard
by visiting this
[link][CVSS_SPECIFICATION].

## Updating the score

On this section, we will give details
on how to update the severity score
for the vulnerabilities, both new and
already reported.

### Locations table actions

This feature allows to update the
severity score for several
or all vulnerabilities at the same time,
whithin a existing type.
First, go to the related
[**Locations table**][LOCATIONS_TABLE],
as shown in the following image.
You must select which vulnerabilities
you want to update,
followed by clicking on the
**Update severity** button.

![Update severity action](https://res.cloudinary.com/fluid-attacks/image/upload/v1673915918/docs/web/vulnerabilities/new-vulnerability-types/new-vuln-severity/update_severity_button.png)

You will get a popup window where
you can edit the severity
using the CVSS severity vector.
A link is present to go to the
[CVSS v3.1 calculator][CVSS_CALCULATOR]
in order to help you derive
the needed string correctly.

![Update severity pop-window](https://res.cloudinary.com/fluid-attacks/image/upload/v1669045647/docs/web/vulnerabilities/new-vulnerability-types/new-vuln-severity/update_severity_popwindow.png)

To save the changes you have made,
click on the **Confirm button**.

### Vulnerability severity tab

In the
[**Locations table**][LOCATIONS_TABLE],
you can click in an specific vulnerability.
Go to the
[**Severity tab**](/tech/platform/vulnerabilities/management/details#severity-tab),
and click the **Edit** button.

![Severity tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1669045647/docs/web/vulnerabilities/new-vulnerability-types/new-vuln-severity/vuln_modal_severity_tab.png)

Enter the modified severity vector,
and click on the **Save button**.
to persits the changes made.

![Severity tab Edit Mode](https://res.cloudinary.com/fluid-attacks/image/upload/v1669045647/docs/web/vulnerabilities/new-vulnerability-types/new-vuln-severity/vuln_modal_severity_tab_edit.png)

### Yaml file

The section
[Reporting vulnerabilities](reporting-vulns)
describes how to use a `.yaml` file
for assigning or even updating
the current severity vector.
Please, refer to it and keep in mind
a valid format must be provided,
according to the
[CVSS v3.1 calculator][CVSS_CALCULATOR].

[CVSS_CALCULATOR]: https://www.first.org/cvss/calculator/3.1
[CVSS_SPECIFICATION]: https://www.first.org/cvss/v3.1/specification-document
[LOCATIONS_TABLE]: /tech/platform/vulnerabilities/management/locations/
