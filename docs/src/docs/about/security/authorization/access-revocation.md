---
id: access-revocation
title: Access Revocation
sidebar_label: Access Revocation
slug: /about/security/authorization/access-revocation
---

When talent go on vacation
or leave the company,
it is essential to revoke their access
to the information and systems
that are available to them.
At `Fluid Attacks`,
we have a two-step process
for access revocation:

1. **Deactivating the IAM account:**
  By doing this,
  users lose access to all company applications
  and client data.
  This includes
  [platform](https://app.fluidattacks.com/),
  mail, etc.

1. **Removing Git repository access:**
  Users can no longer see confidential information
  from the repository,
  such as registry images, private issues,
  [merge requests](https://docs.gitlab.com/ee/user/project/merge_requests/),
  etc.

It is worth noting
that easy access revocation is fundamental
when dealing with sensitive data in an organization.
That is why we have put so much effort
into making this process as simple as possible.

## Requirements

- [023. Terminate inactive user sessions](/criteria/requirements/023)
- [114. Deny access with inactive credentials](/criteria/requirements/114)
- [144. Remove inactive accounts periodically](/criteria/requirements/144)
