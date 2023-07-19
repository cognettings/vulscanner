---
id: members
title: Group level members
sidebar_label: Members
slug: /tech/platform/groups/members
---

The members of a [group](/tech/platform/groups/introduction/)
are the users
who can access it
to visualize information
or manage vulnerabilities,
scope,
tags,
etc.
Only if you have the
[User manager](/tech/platform/groups/roles#user-manager-role)
role,
you can [add,](/tech/platform/groups/members/#add)
[edit](/tech/platform/groups/members/#edit)
or [remove](/tech/platform/groups/members/#remove)
these users.
To use these functions,
you have to go to the
**Members** section
in your group.

![Members Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1684329526/docs/web/groups/members/members_view.png)

## Members table

In total, we have seven columns which are described below:

![Members columns](https://res.cloudinary.com/fluid-attacks/image/upload/v1684329675/docs/web/groups/members/members_columns.png)

- **User email:**
  The user's email address.
- **Role:**
  The role that the user has
  in that organization.
- **Responsibility:**
  The user's responsibility in
  the group.
- **First login:**
  The date and time at which the
  first entry into the organization.
- **Last login:**
  The time recorded since the last entry.
- **Registration status:**
  The state that the user is in can be:
  Registered,
  Unregistered or Pending.
- **Invitation:**
  It allows you to Resend the
  invitation to a user if they
  have yet to accept it.

## Functionalities

In this section,
you will find the
following buttons:

- [Filters.](/tech/platform/groups/members/#filters)
- [Export.](/tech/platform/groups/members/#export)
- [Invite.](/tech/platform/groups/members/#invite)
- [Edit.](/tech/platform/groups/members/#edit)
- [Remove.](/tech/platform/groups/members/#remove)
- [Search bar.](/tech/platform/groups/members/#search-bar)

### Filters

In this section,
you can find the filters on the
left side.

![Filters Icon](https://res.cloudinary.com/fluid-attacks/image/upload/v1684329769/docs/web/groups/members/filters_members.png)

Two filters are available
for the table: [Role](/tech/platform/groups/roles/) and
Registration status.

![Filters Available](https://res.cloudinary.com/fluid-attacks/image/upload/v1684329900/docs/web/groups/members/filters_type.png)

### Export

Clicking on this button will
download a CSV (comma-separated
values) file containing all
the information in the table
of this section.

![Export button](https://res.cloudinary.com/fluid-attacks/image/upload/v1684329988/docs/web/groups/members/export_button.png)

### Invite

Click on invite button to
add a new member.
You will see the following
pop-up window:

![Members invite](https://res.cloudinary.com/fluid-attacks/image/upload/v1684330585/docs/web/groups/members/add_members.png)

Here you must enter information
about the new member:
email,
[role](/tech/platform/groups/roles)
and responsibility.
Bear in mind that we
only accept Azure,
Google or Bitbucket email addresses.

Keep in mind that the user you are adding
has a different email domain that isn't present
in the list of authors;
you will get a warning that it is a user that is part of your company.

![warning](https://res.cloudinary.com/fluid-attacks/image/upload/v1686675706/docs/web/groups/members/warning.png)

When you click the confirm button, the user
will receive an [email](/tech/platform/notifications#access-granted)
asking them to confirm their invitation.

### Edit

The Edit button helps us modify that user's
Role or Responsibility.
First,
you must select the user you want to edit in the check box,
followed by the edit button.

![Members to Edit](https://res.cloudinary.com/fluid-attacks/image/upload/v1684330841/docs/web/groups/members/edit_members.png)

A pop-up window will appear
where you can modify the
information.

![Members Edit](https://res.cloudinary.com/fluid-attacks/image/upload/v1684330934/docs/web/groups/members/member_edit.png)

### Remove

Several members can be removed by
clicking on the checkbox on the left,
where you can mark all the participants
to be removed from the group.

![Remove Checkbox](https://res.cloudinary.com/fluid-attacks/image/upload/v1684331083/docs/web/groups/members/remove_member.png)

After selecting, you go to the Remove button,
where you will get a pop-up window
where you confirm if you want to
remove these participants.

![Remove Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1684331145/docs/web/groups/members/confirm_remove.png)

Clicking this will automatically remove
the selected people from the group.

> **Note:** Keep in mind that all members are automatically
> removed after 90 days of inactivity.

### Search bar

The search bar filters the information
contained in the columns of the table.
