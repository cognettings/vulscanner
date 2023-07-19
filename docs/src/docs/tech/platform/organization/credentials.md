---
id: credentials
title: Credentials
sidebar_label: Credentials
slug: tech/platform/organization/credentials
---

In this section,
you will be able to perform two actions:
[Add credentials](/tech/platform/organization/tech/platform/organization/credentials/#organization-credentials)
at the organization level
and perform the connection via
[OAuth](/tech/platform/organization/tech/platform/organization/credentials/#add-repositories-via-oauth)
to the providers,
which are: **GitLab - GitHub - Bitbucket - Azure**.

## Organization credentials

You can store the credentials at
the organization level and use
them in all the groups that make
up the organization.
To see the credentials that exist,
you have to go to the main page
in the tab called credentials.

![Main Page](https://res.cloudinary.com/fluid-attacks/image/upload/v1670949034/docs/web/credentials/globla_credentials.png)

## Credentials table

Here you can see the list
of all the credentials created
in the organization you are located in.
In total, we have three columns which
are described below:

![Credentials table](https://res.cloudinary.com/fluid-attacks/image/upload/v1683556298/docs/web/credentials/credentials_table.png)

- **Name:**
  The name of the credential.
- **Type:**
  Which type of credential it is,
  can be [HTTPS](/tech/platform/groups/scope/roots#adding-a-root-with-the-https-user-and-password),
  [SSH](/tech/platform/groups/scope/roots#adding-a-root-with-the-ssh-key)
  or [Azure DevOps PAT](/tech/platform/groups/scope/roots#adding-a-root-with-the-azure-devops-pat).
  You can also see in this column the connection
  of the providers via
  [OAuth](/tech/platform/organization/tech/platform/organization/credentials#add-repositories-via-oauth).
- **Owner:**
  The person who created the credential.

## Functionalities​

In the Global Credentials section,
you have four functionalities:

- [Add.](/tech/platform/organization/tech/platform/organization/credentials#add)
- [Edit.](/tech/platform/organization/tech/platform/organization/credentials#edit)
- [Remove.](/tech/platform/organization/tech/platform/organization/credentials#remove)
- [Search bar.](/tech/platform/organization/tech/platform/organization/credentials#search-bar)

### Add

To add an credential,
you have to click on the **Add Credential** button.

![Add individual](https://res.cloudinary.com/fluid-attacks/image/upload/v1679355889/docs/web/credentials/add_credential.png)

Clicking on it will allow you to add via
[OAuth](/tech/platform/organization/tech/platform/organization/credentials/#add-repositories-via-oauth)
or individually.

![Add other](https://res.cloudinary.com/fluid-attacks/image/upload/v1679356577/docs/web/credentials/add_other.png)

Below we show you how to add it individually;
if you want to know how to do it via OAuth,
you can enter [here](/tech/platform/organization/tech/platform/organization/credentials/#add-repositories-via-oauth).

When you click on the Add other,
you will get a pop-up window
where you can add new credentials.

![Add Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1660670043/docs/web/credentials/credent_add_button.png)

Here,
you will have to enter a unique
credential name and select the
credential type (
[HTTPS](/tech/platform/groups/scope/roots/#adding-a-root-with-the-https-user-and-password),
[SSH](/tech/platform/groups/scope/roots/#adding-a-root-with-the-ssh-key)
or [Azure DevOps PAT](/tech/platform/groups/scope/roots#adding-a-root-with-the-azure-devops-pat)).

### Edit

To edit an existing credential,
you have to select which
one you want to edit.
A pop-up window will appear,
where you have to click on
the toggle that says **New secrets**
to enable editing of the credential
and change its information.

![Edit Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1660670043/docs/web/credentials/credent_edit_button.png)

According to the Credential type
will enable the fields for editing.

### Remove

To delete a credential,
you have to select which
one you want to delete;
a warning window will appear
asking for your confirmation.

![Remove Credentials](https://res.cloudinary.com/fluid-attacks/image/upload/v1660670043/docs/web/credentials/credent_remove.png)

The following are some points to
keep in mind regarding credentials:

- If the credential is removed,
  it is also removed from all
  the git roots used.
- When a member is removed
  from the organization,
  then their credentials are
  removed from that organization.
- The owner of the credentials
  is the last one that edited
  the credential's secrets.

### Search bar

The search bar filters the information
contained in the columns of the table.

## Add repositories via OAuth

You can connect directly to code service
providers such as
**GitLab - GitHub - Bitbucket - Azure**
from the
[platform](/tech/platform/introduction)
via **OAuth (Open Authorization)**,
which will allow us to connect Fluid Attacks' platform to the provider,
where users authorize the flow of access
and thus will be able to access all the
repositories that you have in these.

![service providers](https://res.cloudinary.com/fluid-attacks/image/upload/v1676278513/docs/web/credentials/Four_providers.png)

> **Note:** These are the four providers that support
> Fluid Attacks' platform.

We will now perform a step-by-step example using the GitLab provider.

The first step is to go to the **Global Credentials** view,
where you can select the provider of your
convenience that you want to authorize to connect to the platform.

![Gitlab provider](https://res.cloudinary.com/fluid-attacks/image/upload/v1679357013/docs/web/credentials/gitlab_provider.png)

When you click on it,
you will be redirected to the **provider's authorization** page,
where you will be asked to authorize the
connection between Fluid Attacks' platform and your account.
When you click on **Authorize**,
the connection between these two services will be established.

![Authorize provider](https://res.cloudinary.com/fluid-attacks/image/upload/v1676280659/docs/web/credentials/authorize.png)

When you authorize,
you will be redirected to the platform
to the [Global Credentials](/tech/platform/organization/tech/platform/organization/credentials)
view,
where you can see the new credential created as OAuth.

![credential create](https://res.cloudinary.com/fluid-attacks/image/upload/v1676281581/docs/web/credentials/adding_autho.png)

> **Note:** The service you select will no longer
> be shown in since the connection has already been made.

With this connection with your provider
we will be able to access your organization and,
with this,
to all the repositories that you have there.
It will take into account the repositories that
have had activity in the last 60 days.
To see the list of these,
you can do it in the
[Outside](/tech/platform/organization/outside)
section.

![outside](https://res.cloudinary.com/fluid-attacks/image/upload/v1678472033/docs/web/credentials/outside.png)

> **Note:** The list of repositories that are listed
> in this view are repositories that are not associated
> with any group of that specific organization in the platform.
> To see these,
> you must wait about 30 minutes to 1 hour while the
> service connection is made.

## OAuth functionalities

### Remove oauth connection

You can remove the **OAuth credential** by
selecting the credential to be removed followed by the **Remove**
button.

![oauth remove](https://res.cloudinary.com/fluid-attacks/image/upload/v1676282499/docs/web/credentials/remove.png)

> **Note:** The credential will be removed along with
> its repositories listed in the
> [Outside](/tech/platform/organization/outside)
> section.
