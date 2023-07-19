---
id: events
title: Events
sidebar_label: Events
slug: /tech/platform/groups/events
---

Sometimes,
a situation may arise in a
[group](/tech/platform/groups/group-view)
that prevents our analysts
from pentesting part of the
[scope](/tech/platform/groups/scope)
or maybe all of it.
Your team needs to keep track
of these situations and solve them,
so we can resume our assessments.
The place on the [platform](/tech/platform/introduction)
where you can see a cumulative record of
solved and unsolved events in
your group is the Events section.

![Event Tab View](https://res.cloudinary.com/fluid-attacks/image/upload/v1675168760/docs/web/groups/events/events_tab.png)

## Events Table

This section shows a table
providing the following
information:

![Event Table](https://res.cloudinary.com/fluid-attacks/image/upload/v1683814732/docs/web/groups/events/event_table.png)

- **ID:**
  The event’s unique identifier.
- **Root:**
  Refers to the
  nickname of the [root.](/tech/platform/groups/scope/roots#git-roots)
- **Date reported:**
  When the event was reported.
- **Description:**
  The problem that,
  according to the
  hacker,
  impeded,
  or still impedes,
  their security assessments.
- **Type:**
  The category in which
  the problem falls,
  which can be Authorization
  for special attack,
  Incorrect or missing supplies,
  ToE different from what
  was agreed upon or Other.
  You can enter [here](/tech/platform/groups/events#types-of-events)
  if you want to know more about
  the different types of events.
- **Status:**
  The condition of the event,
  which can be Solved,
  Pending, or Unsolved.
  You can enter
  [here](/tech/platform/groups/events/#status-in-the-event)
  if you want to know more.
- **Date closed:**
  When the event was solved,
  if it was;
  otherwise,
  only a hyphen is shown.

## Status in the event

The statuses help us to have more
clarity about the status of our events.
We handle three types:
**Unsolved,**
**Pending,**
and **Solved.**
Here we will explain
the flow of these.

First,
when an event is opened,
it will have the status **Unsolved**.

![Unsolved Status](https://res.cloudinary.com/fluid-attacks/image/upload/v1675168878/docs/web/groups/events/unsolved_status.png)

Here you have to give the
solution to this created event.
When you have it,
go to the checkbox on the
left and click on it.
When you do this,
the **Request Verification** option
will be activated immediately.

![Request Verification Option](https://res.cloudinary.com/fluid-attacks/image/upload/v1675168988/docs/web/groups/events/request_verification.png)

When you click on it,
you will get a pop-up window
where you will have to explain
the justification of how
you solved this event;
remember to enter at least ten characters,
followed by clicking on the **Confirm button**.

![Confirm Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1661276494/docs/web/groups/events/status_confirmb.png)

At this moment,
our event will enter
the **Pending state**,
where we will be waiting
for the verification that
the supplied solution is effective.

![Pending State](https://res.cloudinary.com/fluid-attacks/image/upload/v1675169227/docs/web/groups/events/pending.png)

When validated and the
solution successful,
it will move to our third **Solved state**.

If this solution does not work,
the event will be set to
**Unsolved status**,
and you will receive a
notification where you will see
a comment from the analyst.
These comments will be sent
to you as a
[notification](/tech/platform/notifications/#consulting-digest-notification),
but you can also see them in the
[Consulting](/tech/platform/groups/events#consulting) tab.

## Functionalities

In the events section,
you can see the following functionalities:

- [Filters](/tech/platform/groups/events#filters)
- [Columns filter](/tech/platform/groups/events#columns-filter)
- [Export button](/tech/platform/groups/events#export-events)
- [Request Verification](/tech/platform/groups/events/#request-verification)
- [Search bar](/tech/platform/groups/events#search-bar)

### Filters

By clicking the Filters button,
you can access several filter
options corresponding to the
variables that give columns
their names.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1675169319/docs/web/groups/events/filters.png)

### Columns filter

You can show or hide columns
in the table by clicking on
the Columns button and toggling
the on/off button in front
of each column name.

![Columns Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1674846579/docs/web/groups/events/funct_filter_columns.png)

### Export

You can download the event table
to a CSV (comma-separated values)
file by clicking on the Export button.

![Export file](https://res.cloudinary.com/fluid-attacks/image/upload/v1682622139/docs/web/groups/events/export_file.png)

### Request Verification

Once you have the solution for the open event,
you can request a solution revision.
See the
[status in the event](/tech/platform/groups/events#status-in-the-event)
section for more information on this workflow.

![Request verification button](https://res.cloudinary.com/fluid-attacks/image/upload/v1683815893/docs/web/groups/events/request_veri.png)

### Search bar

The search bar filters the information
contained in the columns of the table.

## Event details

When you select an event,
you access a new section
with its **Details.**
This section is composed of three
subsections which are:
Description,
Evidence,
and Consulting.

It also has an information header
that shows the title of the event
type along with its ID,
the Date reported,
and the Current status of the event.

![Event Details Header](https://res.cloudinary.com/fluid-attacks/image/upload/v1674847263/docs/web/groups/events/header.png)

### Description

In **Description**,
you find why the event
was reported by one of
our hackers along
with their email,
the site where it is
present and the number
of components affected.

![Event Details Description](https://res.cloudinary.com/fluid-attacks/image/upload/v1674847360/docs/web/groups/events/description_tab.png)

### Evidence

Next is **Evidence** tab,
you find images with **.png** and
**.jpg** extension and videos
with the **WebM** extension,
helping us to understand
the reported event.

![Event Details Evidence](https://res.cloudinary.com/fluid-attacks/image/upload/v1671735595/docs/web/groups/events/evidence_view.png)

### Consulting

In **Consulting**,
you find the discussion
established between your
company's staff and
`Fluid Attacks` hackers or
project managers about the event.
You can leave your comments there.

![Event Details Consulting](https://res.cloudinary.com/fluid-attacks/image/upload/v1674847565/docs/web/groups/events/consulting_view.png)

> **Note:** The Consulting section is only available for the Squad plan.

## Types of events

The event can be reported for different causes.
Here are all the different types.

### Network access issues

The network port no
longer has internet access.

### VPN issues

Fails on the VPN connection.

### Remote access issues

Problems with connection methods.
For example,
when access to environmental
is not possible.

### Authorization special attack

A specific test needs to be performed,
which may affect availability
or integrity and requires
permission by the customer
to carry out a specific test.

### Client cancels project milestone

Customer cancels projects.

### Client explicitly suspends project

The client suspends the
project for a specified
time or excludes a
particular part of the ToE.

### Cloning issues

Some repository does not clone.

### Credential issues

No credentials exist,
or those that do exist
are not valid.

### Data update required

Reset user credentials or
data changes to consume a service.

### Environment issues

Problems in the environment,
either because it does not
open or because some flow
inside it has functional problems.

### Installer issues

Unable to install or error
when installed on mobile
or desktop application.

### Missing supplies

Lack of supplies
other than credentials.

### TOE differs approved

In Continuous Hacking,
there are services
different from those agreed upon
or non-existent functionalities.

### Other

Any other problems that do not
fall into the above categories.
