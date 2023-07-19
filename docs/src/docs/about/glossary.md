---
id: glossary
title: Glossary
sidebar_label: Glossary
slug: /about/glossary
---

## CVSS

The Common Vulnerability Scoring System or CVSS
is a free and open industry standard
for assessing the severity
of computer system security vulnerabilities.
CVSS attempts to assign
severity scores to vulnerabilities,
allowing responders to prioritize responses
and resources according to threat.
Scores are calculated based on a formula that
depends on several metrics
that approximate ease of exploit
and the impact of exploit.
Scores range from 0 to 10,
with 10 being the most severe.

## CVSSF

The CVSSF metric is a creation of `Fluid Attacks.`
It shows the level of **risk exposure**
represented by the vulnerabilities in your system.
The **CVSSF** allows an aggregate analysis
of vulnerabilities.
The scale that is handled is from 0.015625 to 4096.

## Mailmaps

These are the rules
that must be followed
at the time of
documenting the mailmap:

1. Use the email address
  of the provider
  over the one
  of the client.
    - Use `<eduardo.garcia@company.com>`
      over `Eduardo Garcia` `<eduardo.garcia@corporation.com>`
      or `EduardoGarcia` `<egarcia@institute.edu.co>`.
1. Do not map by default
  a non-corporate email
  such as
  `userdeveloper <user123@gmail.com>`.
1. In order to map
  a non-corporate email
  to a corporate one,
  written request
  from the client
  is required.

## Health Check

Consists of performing manual tests
on the previously developed system
before the Squad plan service starts.
Vulnerabilities are identified,
exploited,
and in a complete way
(code,
application,
and current system infrastructure).

> **Note:** The Health Check is optional,
> but if it is not executed,
> there will be parts of the application
> that will never be tested and,
> therefore,
> vulnerabilities with the risk of exploitation.
> If the health check is not performed,
> the accuracy SLA does not apply.

## ToE

The Target of Evaluation or ToE
is the product or system
that will be the subject
of the penetration testing
done by `Fluid Attacks`.
The ToE is mostly defined by specifying
which git repositories and/or environments
you want us to check
by adding Git Roots
and its environments
in the Scope section of a group.

> **NOTE:**
> This subsection of our documentation is under construction.

## White box

The white box is a service where
the hacker has all the information
privileges such as Git roots,
credentials,
source code and environments.

## Black box

The black box is a service where
the hacker does not have access to
source code or information of the
IT structure of the project,
having only access to IP and URL,
environments being these services deployed.

## Continuous integration (CI)

CI is a practice in which a development team
constantly uploads changes,
either additions or removals,
to a central repository.
Automated procedures are run each time to
validate that the modifications made to
the code meet predefined requirements
and to ensure that they integrate smoothly into the software.

## Continuous deployment (CD)

CD is a process that follows CI.
When merged,
the different code changes made by developers
shape a software product that can be deployed
in a test or production environment.
Automated procedures are executed to build the product,
verify that it meets acceptance requirements and perform
a proper deployment at the expected time,
often directly to the end users.

### CI/CD pipeline

This pipeline is a series of organized steps or tasks that,
mainly in an automated way,
allow the successful and fast release of a new software version.
Among the activities that take place are the
compilation of the source code,
the distribution of packages,
the execution of quality and security tests and
the deployment to different environments.

## Static application security testing (SAST)

SAST is a security testing technique for identifying
security vulnerabilities in an application's source code.
It examines the non-running code to look for programming patterns,
misconfigurations and insecure practices that attackers could exploit.

## Dynamic application security testing (DAST)

DAST is a security testing technique for detecting
security vulnerabilities in an application.
It assesses the running software without
accessing its source code,
using various attack vectors in search of
unexpected behavior and weaknesses related
to its deployment configuration, data and business logic.
