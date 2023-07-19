---
id: roles
title: Roles
sidebar_label: Roles
slug: /tech/platform/groups/roles
---

Users on Fluid Attacks' platform have different
roles with associated permissions
relevant to work on the platform.
Depending on your role,
you are granted access to certain
functions for your daily use
of the platform.
You can see your role on Fluid Attacks' platform in the
[drop-down menu](/tech/platform/user)
that appears when you click the
user icon on the upper-right
part of your screen.

The following are the different
roles that are available on the platform,
along with their descriptions.

## User manager role

This is the role
that gives the user
the most privileges,
this user can do everything
that a client is allowed to do
in the platform.
This role is made for
the leaders of the product
and, besides the basic privileges,
it allows the user to generate reports,
define important treatments like
accepting vulnerabilities permanently,
requesting Zero Risk treatments,
adding and editing users for the group
and more.

## User role

This is the default user role,
it is the one given to developers
or the users in charge of
solving the vulnerabilities.
This user can check all the information
about the vulnerabilities
needed for solving them
and also request reattacks
when they deem them solved.

## Vulnerability manager role

The role of vulnerability
manager was designed for
people with a position as
technical leaders in their
company.
This role has access to the
basic privileges on the platform
and is also enabled to
generate reports;
get notifications;
define,
change and approve treatments;
request reattacks,
and add tags.
The vulnerability manager
**does not** have permissions
to manage roots nor add,
edit or remove users.

## Functions

- **Create an Organization:**
  Creating an organization on our
  platform centralizes and organizes
  information in one place.
- **Create a Group:**
  By creating a group,
  you can manage vulnerabilities by project.
  For more information,
  click [here.](/tech/platform/groups/group-view/#scope-overview)
- **Notify button:**
  This feature helps us notify all open locations
  of the specific vulnerability type,
  receiving a report of these.
- **Add roots:**
  This function is for
  adding git roots
  to the scope of the group
  being managed.
- **Add tags:**
  This is for adding tags
  to the group being managed
  which is useful for
  categorizing different groups
  in an organization.
- **Add users:**
  This function is for
  adding user to a group
  and setting their privileges.
- **Approve treatments:**
  This function is for
  when a treatment change is requested,
  as there is a need to validate
  and then accept or reject
  this request.
- **Change treatments:**
  Each vulnerability can be given
  a specific treatment.
  This function gives the ability
  to request the change
  of this treatment.
- **Deactivate/Activate root:**
  This function allows you to:
  1. Deactivate repositories
     for which you no longer want
     an assessment;
  1. Activate repositories you want
     to leave available to our analysts,
     and
  1. Move a root to another group,
     taking all the associated
     vulnerabilities with it.
- **Delete groups:**
  With this function
  you are able to
  completely delete
  the group being managed.
- **Edit roots:**
  This function allows you
  to change URLs of roots
  that do not have reported
  vulnerabilities and edit
  root branches.
- **Edit users:**
  This option is for
  editing everything related
  to the users added
  to the group.
- **Exclusions:**
  This feature allows you
  to choose files or folders
  in your repository that
  you do not want to
  include in the security
  assessments.
- **Generate a report:**
  This feature allows you
  to generate and download
  a complete report with
  detailed information about
  the vulnerabilities of
  a specific group.
- **Generate a certificate:**
  Generates a security testing certification.
- **Receive notifications:**
  This is the ability to
  receive notifications
  that Fluid Attacks' platform can send
  related to your group.
- **Request reattacks:**
  When a vulnerability is solved,
  there is the need to ask our hackers
  to verify that it was indeed solved.
  This function gives you
  the ability to make
  this kind of request.
- **View vulnerabilities:**
  The ability to view
  all the information available
  about all the vulnerabilities
  that the project has.
- **Vulnerability report Analytic:**
  Download your organization's
  vulnerabilities
  (including all vulnerability statuses)
  in a .CSV file.
  For more information,
  click [here.](/tech/platform/analytics/reports#vulnerabilities-download)
- **OAuth connection:**
  Connection between the providers
  GitLab - GitHub - Bitbucket - Azure
  with the platform.
- **Add Outside repositories:**
  Repositories that are not yet part of any
  group of the organization.
  You can add them in bulk or as a unit
  in your required group.
- **Edit group information:**
  Be able to edit the
  [group information.](/tech/platform/groups/scope/other-sections/information)
  This section is located in **Scope -> Information.**
- **Edit a vulnerability:**
  With this functionality,
  you can edit the vulnerability,
  give the assignment and treatment,
  adding tags,
  among others.
- **vulnerability assignment:**
  Assign any vulnerability to a member of your team.
  For more information,
  you can access this
  [link.](/tech/platform/vulnerabilities/management/to-do/)
- **Consulting:**
  You can communicate all the questions,
  requests,
  suggestions,
  and matters concerning your group or a specific
  vulnerability or event that require much more
  direct interaction.
- **Agent Token generation:**
  Generate the agent token to run it.
- **Run the agent:**
  Execute the agent in your pipelines or CI/CD.

## Roles table

In the following table
we specify
what functions are enabled
for each role.

|                              | User | Vulnerability manager | User manager |
| ---------------------------- | :--: | :-------------------: | :----------: |
| Create an Organization       |  X   |                       |      X       |
| Add roots                    |  X   |                       |      X       |
| Add tags                     |  X   |           X           |      X       |
| Add users                    |      |                       |      X       |
| Approve treatments           |      |           X           |      X       |
| Change treatments            |  X   |           X           |      X       |
| Deactivate/Activate root     |      |                       |      X       |
| Delete groups                |      |                       |      X       |
| Edit group information       |      |                       |      X       |
| Edit roots                   |  X   |                       |      X       |
| Edit users                   |      |                       |      X       |
| Exclusions                   |      |                       |      X       |
| Generate a certificate       |      |                       |      X       |
| Generate a report            |      |           X           |      X       |
| Group policies               |      |                       |      X       |
| Receive notifications        |  X   |           X           |      X       |
| Request reattack             |  X   |           X           |      X       |
| View vulnerabilities         |  X   |           X           |      X       |
| Vulnerability report Analytic|      |                       |      X       |
| support channels             |  X   |           X           |      X       |
| OAuth connection             |      |                       |      X       |
| Add Outside repositories     |      |                       |      X       |
| Compliance Report            |  X   |           X           |      X       |
| Add ORG credentials          |      |                       |      X       |
| ORG policies                 |      |                       |      X       |
| Create a Group               |      |                       |      X       |
| Notify button                |      |           X           |      X       |
| Consulting                   |  X   |           X           |      X       |
| Edit a vulnerability         |  X   |           X           |      X       |
| vulnerability assignment     |  X   |           X           |      X       |
| Agent installation           |  X   |           X           |      X       |
| Agent Token generation       |  X   |           X           |      X       |
| Run the agent                |  X   |           X           |      X       |
| Request verification events  |  X   |           X           |      X       |
| Create portfolio             |  X   |           X           |      X       |
| Add secrets                  |      |                       |      X       |
| Unsubscribe groups           |  X   |           X           |      X       |
| Generate API token           |  X   |           X           |      X       |

## Internal roles

`Fluid Attacks’` internal roles on Fluid Attacks' platform.

### Hacker

The hacker is a security analyst
whose main objectives are identifying,
exploiting and reporting vulnerabilities
in organizations' systems.

### Reattacker

The reattacker is in
charge of verifying,
through diverse techniques,
the effectiveness of the
solutions implemented by the
organizations for vulnerability
remediation.

### Customer manager

The customer manager mainly provides
support and streamlines processes
of the organizations.
For example,
on the platform,
they can make changes
in group information,
request reattacks,
generate reports and
manage members,
among many other things.

### Resourcer

The resourcer helps keep updated
the inputs provided by the organizations,
such as environment credentials
and mailmap authors,
among others.

### Reviewer

The reviewer is in charge of
managing the vulnerabilities
that are reported to the
organizations.
They evaluate drafts for
approval or disapproval,
request reattacks and verify
and notify which vulnerabilities
are zero risk.

### Architect

The architect's main objective
is to ensure the highest quality
of ethical hacking and pentesting
deliverables.
Among their functions are deleting
false positives or errors,
including or deleting evidence,
and providing help to the
organizations over the support channels.

### Admin

The admin is the one who has all
the privileges on Fluid Attacks' platform,
except for the possibility
to change treatments.

## Internal roles table

In the following table,
we specify what functions are
enabled for each role:

|                          | Hacker | Reattacker | Resourcer | Reviewer | Architect | Customer Manager | Admin |
| ------------------------ | :----: | :--------: | :-------: | :------: | :-------: | :--------------: | :---: |
| Add drafts               |   X    |     X      |           |          |     X     |                  |   X   |
| Add events               |   X    |     X      |     X     |          |     X     |        X         |   X   |
| Add roots                |        |            |           |          |           |        X         |   X   |
| Approve drafts           |        |            |           |    X     |           |                  |   X   |
| Change treatments        |   X    |            |           |          |     X     |                  |       |
| Confirm/Reject ZR        |        |            |           |    X     |     X     |                  |   X   |
| Deactivate/Activate root |        |            |           |          |           |                  |   X   |
| Delete groups            |        |            |           |          |           |        X         |   X   |
| Edit roots               |        |            |           |          |     X     |                  |   X   |
| Generate a report        |   X    |            |           |          |     X     |        X         |   X   |
| Manage evidences         |   X    |            |           |          |     X     |                  |   X   |
| Request reattack         |   X    |     X      |     X     |    X     |     X     |        X         |   X   |
| Request ZR               |        |            |           |          |           |        X         |   X   |
| Solve events             |   X    |     X      |     X     |          |     X     |        X         |   X   |
| Verify reattack          |   X    |     X      |           |          |     X     |                  |   X   |

:::tip free trial
**Search for vulnerabilities in your apps for free
with our automated security testing!**
Start your [21-day free trial](https://app.fluidattacks.com/SignUp)
and discover the benefits of our [Continuous Hacking](https://fluidattacks.com/services/continuous-hacking/)
[Machine Plan](https://fluidattacks.com/plans/).
If you prefer a full service
that includes the expertise of our ethical hackers,
don't hesitate to [contact us](https://fluidattacks.com/contact-us/)
for our Continuous Hacking Squad Plan.
:::
