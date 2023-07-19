---
id: group-view
title: Group view
sidebar_label: Group view
slug: /tech/platform/groups/group-view
---

The groups correspond to single
projects that our clients create
to manage their vulnerabilities
separately.
You may have several
groups corresponding to
separate applications,
infrastructure or source code.
When you create a group,
the ethical hackers at
`Fluid Attacks` start
assessing it in search
for vulnerabilities.

## Scope overview

In the Groups view,
you will find **Scope Overview**,
which will give you global and visible
information on the total of
[repositories](/tech/platform/groups/scope/roots#git-roots)
and
[authors](/tech/platform/groups/authors)
you have in Fluid Attacks' platform.
You will find the following fields:

![scope overview box](https://res.cloudinary.com/fluid-attacks/image/upload/v1675160701/docs/web/groups/general/scope_overview.png)

- **Covered authors:**
  Total number of authors who
  have made commits to the repositories.
- **Covered repositories:**
  Total number of repositories at
  the organization level that are
  added for the source code analysis.
- **Missed authors:**
  Total number of authors who have
  made commits on the missed repositories
  (repositories [Outside](/tech/platform/organization/outside)).
- **Missed repositories:**
  How many repositories are not
  included in the source code analysis.
  (You can find these repositories in
  the **Outside** section).

Clicking on any of these four boxes
will redirect you to the
**Outside** section.
If you want to know more about this section,
click [here](/tech/platform/organization/outside).

## Group table

In the group table,
you find all the groups you
have access to within your
[organization.](/tech/platform/organization/introduction)
This table has seven columns,
each of which allows you to
organize the list content
alphabetically (either
ascending or descending) if
you click on the arrows next
to each title.

![Group Table columns](https://res.cloudinary.com/fluid-attacks/image/upload/v1675160905/docs/web/groups/general/groups_table.png)

You find the following information:

- **Group name:**
  The first column shows you
  the names of the groups.
- **Group status:**
  You can find three options:
  **Subscribed**,
  **Free-trial** and
  **Suspended**.
  **Subscribed** is when the method
  of payment is valid, **Free-trial**
  you find it when the group is
  part of Enrollment
  and **Suspended** means
  payment methods are being analyzed,
  or the Free-trial has been completed.
- **Plan:**
  You can see the plan to which each
  group belongs.
- **Vulnerabilities:**
  Typologies that have any unsolved location.
- **Description:**
  The next column gives you the
  short descriptions the groups
  received at their creation.
- **Role:**
  The [role](/tech/platform/groups/roles)
  within each of them.
- **Events:**
  The last column tells you how
  many unsolved events each group
  has (to learn more about this column,
  we invite you to
  [click here](/tech/platform/groups/group-view/#unsolved-events)).

> **Note:** When you enter a group,
> following the link in its name,
> you can see its detailed information
> in different subsections,
> which will vary depending on
> your [role](/tech/platform/groups/roles/) and the plan you have
> for that group.

![Vulnerabilities view](https://res.cloudinary.com/fluid-attacks/image/upload/v1675161219/docs/web/groups/general/vulnerabilities_view.png)

## Functionalities

In the group's section,
you can see the following functionalities:

- [Create new group](/tech/platform/groups/group-view/#create-new-group)
- [Group filters](/tech/platform/groups/group-view/#group-filters)
- [Search bar](/tech/platform/groups/group-view/#search-bar)
- [Edit/Delete a Group](/tech/platform/groups/group-view/#edit-or-delete-a-group)

### Create new group

To start creating a new group,
you need to click on the
**New group** button in the
main screen of your organization.

![New Group Option](https://res.cloudinary.com/fluid-attacks/image/upload/v1675161304/docs/web/groups/general/create_new_group.png)

A pop-up window will appear
to set up the characteristics
of your new group.
You will be asked to provide
the following:

- **Organization:**
  Name of the organization in
  which the group is to be created.
- **Group name:**
  Enter a name for your group.
  It is recommended to choose a
  short one that is easy to remember.
- **Description:**
  Write a description that
  will help you identify the
  project to which that
  group is associated.
- **Type of service:**
  Select between Continuous Hacking - Machine Plan
  and Continuous Hacking - Squad Plan.
- **Type of testing:**
  Select between [white-box](/about/glossary/#white-box)
  and [black-box](https://docs.fluidattacks.com/about/glossary/#black-box)
  testing.
- **Report language:**
  Select a language in which
  you would like your reports
  to be.

![Types](https://res.cloudinary.com/fluid-attacks/image/upload/v1669032582/docs/web/groups/general/creating_gruop.png)

When you are finished
setting up your new group,
you can click **Confirm**.
The group will be added to
your group table immediately,
and you will be all set to
start working on your project.

### Group filters

Filters allow you to limit
the data you visualize,
facilitating your search.
The Group section has a
**Filters** button which,
upon click,
allows you to filter your
group search by either group
name or plan
(Machine Plan or
Squad Plan).

![Group Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1667250616/docs/web/groups/general/group_filtes.png)

### Search bar

The search bar filters the information
contained in the columns of the table.

### Edit or delete a Group

You can [edit](/tech/platform/groups/scope/other-sections/context)
or [remove](/tech/platform/groups/scope/other-sections/delete) a group
in its [Scope](/tech/platform/groups/scope) section.

## Open eventualities

### Unsolved events

In the group table,
you find a column
called **Events.**
In this column,
you can discover how many
unsolved [events](/tech/platform/groups/events) need your
attention in each of your groups.

![Unsolved Events Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1675161566/docs/web/groups/general/open_even.png)

When you enter one of the
groups with at least one
unsolved event,
you can notice a red dot
in the Events tab,
which works as a warning
signal that something
requires your intervention.

![Warning Signal](https://res.cloudinary.com/fluid-attacks/image/upload/v1674777821/docs/web/groups/general/event_alert.png)

When you click that tab,
you see the event table
with a Status column showing
for each event whether it is
solved (in green), unsolved
(in red) or pending (in yellow).

![Status Column](https://res.cloudinary.com/fluid-attacks/image/upload/v1675161767/docs/web/groups/general/status_event.png)

If you want to know more about the event section,
you can enter [here.](/tech/platform/groups/events)
