---
id: roots
title: Roots
sidebar_label: Roots
slug: /tech/platform/groups/scope/roots
---

In this section of the Scope tab,
you can add and edit the repositories
and environments to be included
in the testing service.
If you want to know more
about these service types,
click [here](/tech/platform/groups/scope/other-sections/services).

If your group has
[White services](/about/glossary/#white-box)
it will have [Git Roots](/tech/platform/groups/scope/roots/#git-roots)
and [Environments](/tech/platform/groups/scope/roots/#environments-table),
or if your group has [Black services](/about/glossary/#black-box),
you will have [IP Roots](/tech/platform/groups/scope/roots/#ip-roots)
and [URL roots](/tech/platform/groups/scope/roots/#url-roots).

## Git Roots

Here we put any Git repositories
composed of code to clone and
start the analysis of these.
In Git Roots,
you can
[add,](/tech/platform/groups/scope/roots/#add-new-root)
[edit,](/tech/platform/groups/scope/roots/#managing-git-root)
enable or [disable](/tech/platform/groups/scope/roots/#deactivate-a-git-root)
the root.
You can also [export](/tech/platform/groups/scope/roots/#export-button) and [filter](/tech/platform/groups/scope/roots/#columns-filter)
the information of all your
Roots that compose the [table.](/tech/platform/groups/scope/roots/#git-roots-table)

## Git Roots table

The Git Roots table gives us
summary information of the
repositories I want to be analyzed.

![Git Root table](https://res.cloudinary.com/fluid-attacks/image/upload/v1668103427/docs/web/groups/scope/git_root_table.png)

This table shows the following information:

- **URL:**
  Refers to the URL of the
  repository where the code
  to be cloned is located.
- **Branch:**
  The branch I am going to clone.
  Remember we assess only one
  repository branch per group.
  For more information click
  [here.](/tech/platform/groups/scope/roots/#single-root-assessment)
- **State:**
  There are two states:
  **Active and Inactive**.
  **Active** means that the root
  is being tested and
  **Inactive** means that the root
  is no longer being tested.
- **Status:**
  There are six:
  Cloning,
  OK,
  Failed,
  N/A, Queued and Unknown.
  For more information click
  [here.](/tech/platform/groups/scope/roots/#status-in-git-root)
- **HCK:**
  If [Health Check](/about/glossary#health-check)
  is included
  in that repository.
- **Nickname:**
  The nickname of this repository
  to be easily identified.
- **Sync:**
  Request to clone that repository
  once again since changes have been
  generated and it is required to
  have it updated.

There is also a **downward-facing arrow**
on the left of the Type column,
which,
upon click,
will unfold the description for
each repository.

![Downward-facing arrow](https://res.cloudinary.com/fluid-attacks/image/upload/v1668103621/docs/web/groups/scope/downward.png)

## Git Roots functionalities

### Add new root

To add a new Root,
you must click on the button **add new root.**
You can add a new repository using
**Oauth (Open Authorization)** or
**manually.**

![Add button](https://res.cloudinary.com/fluid-attacks/image/upload/v1686917372/docs/web/groups/scope/add_button.png)

We will explain each of these below.

#### Adding repositories via OAuth

You can easily add repositories with **Oauth**
from **Gitlab,**
**Github,**
**Bitbucket**
or **Azure**.
To start using this functionality,
you must first add a credential in the
**""Global Credentials"**  section.
To learn more about this section,
you can enter [here.](/tech/platform/organization/tech/platform/organization/credentials/#add-repositories-via-oauth)

Once you have added a **Credential**,
select the provider where you have them registered.

![Provider](https://res.cloudinary.com/fluid-attacks/image/upload/v1686917759/docs/web/groups/scope/provider.png)

For this documentation,
we will perform the example with the GitLab provider.
When you click on this,
you will get a box where you will be asked to
choose which user is the credential,
listing all users who are part of that group
and have an OAuth connection with that same provider.

![Owner the credential](https://res.cloudinary.com/fluid-attacks/image/upload/v1686917965/docs/web/groups/scope/owner.png)

When selecting the credential,
it will read all the data from its repositories
and their branches
(keep in mind that depending on the data,
it may take some time to load).
When finished,
it will activate the continue button.

![Credential selected](https://res.cloudinary.com/fluid-attacks/image/upload/v1686918166/docs/web/groups/scope/owner_of_credential.png)

When you click continue,
you will be presented with a form that consists of three steps:
Choose Repositories,
Select Repository Branch and Exclusions,
and Health Check.

![Three steps](https://res.cloudinary.com/fluid-attacks/image/upload/v1686918254/docs/web/groups/scope/three_steps.png)

In the first part of adding repositories,
it will list the repositories that are not
yet loaded on the platform,
and you can search for them in the search bar
or select them in the check box.
Each repository you choose will activate a field called
**Environment kind (Type of environment that is this root),**
which can be production, QA, development, etc.

![Enviroment kind](https://res.cloudinary.com/fluid-attacks/image/upload/v1686918402/docs/web/groups/scope/enviroment_kind.png)

When you fill in the type of environment,
the Next Step button will be activated;
you will select the branches with those selected repositories.

![Branches](https://res.cloudinary.com/fluid-attacks/image/upload/v1686918568/docs/web/groups/scope/branchses.png)

Once you have selected these,
you can continue to the last step.
You can also click the Previous button to return to the previous step.

You will be asked two questions in the
[Exclusions](/tech/platform/groups/scope/exclusions)
and [Health Check](/about/glossary/#health-check) section.
First,
**Are there files in your selection that you want the scans to ignore?**
When you click on Yes,
it will activate the fields for you to enter which file,
folder,
or path you want to ignore;
if you have doubts about exclusions,
you can enter
[here.](/tech/platform/groups/scope/exclusions)

As a second question,
you will be asked Health check:
**Would you like a health check for the existing code?**
Where you can decide with a yes or no.

![Final steps](https://res.cloudinary.com/fluid-attacks/image/upload/v1686919255/docs/web/groups/scope/final_steps.png)

When you finish filling in the three fields,
Add root will be activated,
where you will add them successfully.
This way,
you can add several repositories in only three steps.

#### Add new root manually

To add a new Root,
you must click on the
box **add new root**.

![Adding action](https://res.cloudinary.com/fluid-attacks/image/upload/v1682973987/docs/web/groups/scope/add_button.png)

There you will get a pop-up
window where you will have to
enter the information of the
new repository you want to add.

![Add New Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668103688/docs/web/groups/scope/add_new_gitroot.png)

The information you have to fill in is as follows:

- **URL:**
  The URL where the
  repository is located.
- **Branch:**
  The branch that is inside
  the repository that I want
  to be validated.
- **Use VPN:**
  You can specify that to have access
  to the inputs you provide;
  we need to connect to the your private network.
- **Existing credentials:**
  These credentials have been created and used,
  you can be reused.
  For more information,
  click
  [here](/tech/platform/groups/scope/roots#existing-credentials).
- **Credential Type:**
  To have access to the repository,
  we have to have access to
  the credentials,
  which are three types:
  [HTTPS](/tech/platform/groups/scope/roots/#adding-a-root-with-the-https-user-and-password),
  [Azure DevOps PAT](/tech/platform/groups/scope/roots/#adding-a-root-with-the-azure-devops-pat)
  and
  [SSH](/tech/platform/groups/scope/roots/#adding-a-root-with-the-ssh-key).
  Here,
  you select which type of
  credential you want to add.
  For more information,
  click [here.](/tech/platform/groups/scope/roots/#credential-type)
- **Environment kind:**
  The type of environment that is this root.
- **Exclusions:**
  Specifies what files of that
  root will be ignored during
  the analysis by clicking on
  the **Yes button,**
  then you can add many as you need.
  If you want to know how to do it,
  you can enter [here](/tech/platform/groups/scope/exclusions).
- **Health Check:**
  You have to put YES or NO
  if this git root applies
  [Health Check.](/about/glossary#health-check)

When you fill in the required fields,
click on **Confirm**,
and your repository will
be successfully added.

### Export button

Clicking on the **Export**
button will download a file
with CSV (comma-separated
values) extension,
which contains the information
in the Git Root table.

![Export button](https://res.cloudinary.com/fluid-attacks/image/upload/v1683031998/docs/web/groups/scope/export_gitroot.png)

### Columns filter

Columns filter helps us to
show or hide which columns I
want to see in the Git Roots table.
By clicking on the toggling
on/off button in front
of each column name,
you can manipulate the
information to display
in the table.

![Columns Filter](https://res.cloudinary.com/fluid-attacks/image/upload/v1668104380/docs/web/groups/scope/columns_filter.png)

### Filters

We have five different filters
in the Git Roots section,
helping us filter the information
that is of interest quickly and safely.

![Filters](https://res.cloudinary.com/fluid-attacks/image/upload/v1668104488/docs/web/groups/scope/general_filters.png)

### Managing Git Root

If you want to **edit** the details
of an active root,
you need to click on it.
A pop-up window will appear,
where you can navigate three tabs:
[Git repository](/tech/platform/groups/scope/roots/#git-roots),
[Environments](/tech/platform/groups/scope/roots/#environments-table)
and [Secrets.](/tech/platform/groups/scope/roots/#secrets)

![Managing Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668171709/docs/web/groups/scope/managing_git_root.png)

The Git repository tab allows you
to change details of your Git root.
Keep in mind that modifying the
repository’s URL and branch is only
allowed if absolutely no vulnerabilities
have been reported in it.
If there are reported vulnerabilities,
you will have to add a new root
with the URL and branch you need
to include in the security tests.

If you want to know how to edit
or add an environment,
enter [here](/tech/platform/groups/scope/roots/#managing-git-root-environments).
Now,
if you're going to add or edit secrets,
you can learn how to do it
[here](/tech/platform/groups/scope/roots/#secrets).

> **Note:** You can enter the root **nickname** by doing the edit action.

### Deactivate a Git Root

:::caution
Scope changes may involve closing or reporting new vulnerabilities
:::

Deleting a root isn't possible
in Fluid Attacks' platform because in the
security world it is
always better to keep
records of everything.
However,
you can change its state
to **Active** or **Inactive**,
which would mean the following:

- **Active:**
  The repository is available and ready for our analysts to access.
- **Inactive:**
  The repository does not exist anymore, it was changed, or it was added by
  mistake.

We will notify the state changes
via email to all the people involved in the
project (both `Fluid Attacks`
and the customer’s users).

You can change the state at any moment.
We will keep track of every change for
traceability reasons.

To do this action of change of state,
you must first find the branch
you want to disable or move to.
Once you know which one it is,
go to the state column and
click on the toggle of the
branch that is currently active.

![Deactivate Git Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668182871/docs/web/groups/scope/toggle_brach.png)

Here,
you will get pop-up window
asking why you want to
disable the root.

![Deactivate Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1683034357/docs/web/groups/scope/deactivate_root_windw.png)

When you click on the drop-down menu,
you will get three options:
[Registered by mistake,](/tech/platform/groups/scope/roots/#registered-by-mistake)
[move to another group,](/tech/platform/groups/scope/roots/#moved-to-another-group)
and [other.](/tech/platform/groups/scope/roots/#other)

#### Registered by mistake

This option is useful in case
of mistakes when adding a root,
but if you just
need to update the URL,
branch or any other root attributes,
refer to [Managing Git Root](/tech/platform/groups/scope/roots/#managing-git-root).

#### Moved to another group

This option allows moving a
root to another group along with the
vulnerabilities reported to it.

![Move root](https://res.cloudinary.com/fluid-attacks/image/upload/v1668183656/docs/web/groups/scope/move_other_group.png)

The search bar will suggest
other [groups](/tech/platform/groups/introduction/)
with the same
service type that you have
access to within the organization.

#### Other

When neither of the previous two
reasons applies,
then you can use this one and
put what the reason is.

![other reason](https://res.cloudinary.com/fluid-attacks/image/upload/v1683034746/docs/web/groups/scope/other_reason.png)

## VPN

We know that for security reasons,
you want to keep in your internal
network your repositories,
applications,
or confidentiality issues that are
handled in your company,
where it is necessary to access these
by connecting to the
**VPN (Virtual Private Network).**

When creating a
[Root](/tech/platform/groups/scope/roots/#git-roots)
in [Scope,](/tech/platform/groups/scope/) or edit this
you can specify that to have
access to the inputs you provide;
you need to connect to the private
network by clicking on the check
box that says **Use VPN.**

![VPN](https://res.cloudinary.com/fluid-attacks/image/upload/v1672265483/docs/web/groups/scope/vpn.png)

Telling us this our engagement team
start all the process to configure
and establish a site to site VPN
to access the internal network and
cloning the repositories you offer us.

## Credential Type

To clone a Git repository in
the [Scope](/tech/platform/groups/scope) section,
you can do it with:
[**Protocol HTTPS (User and Password),**](/tech/platform/groups/scope/roots/#adding-a-root-with-the-https-user-and-password)
[**SSH key (Security Shell)**](/tech/platform/groups/scope/roots/#adding-a-root-with-the-ssh-key)
or [**Azure Organization (Access Token).**](/tech/platform/groups/scope/roots/#adding-a-root-with-the-azure-devops-pat)
You can use any of these for authentication.

> **Note:** We deduce the type of credential from
> the repository URL that you provide.

### Adding a root with the HTTPS​ (User and Password)​

With HTTPS you can access by
putting **User** and **Password**.

![Adding Root HTTPS](https://res.cloudinary.com/fluid-attacks/image/upload/v1670942450/docs/web/groups/scope/https.png)

Remember that the **Check Access**
button helps us to validate if the
access credentials given are
correct to perform the
cloning successfully.
If they are not,
you will get invalid Credentials,
and if they are valid,
you will get Success access.

> **Note:** If you clone via **HTTPS** with **GitHub**,
> you must replace the **password** with a **personal token**.
> To generate this token,
> you can go to the official Github documentation
> [link](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token).

### Adding a root with the SSH key

With SSH keys,
you can connect to your repository
server without using a username and password.
Here you have to supply a Private Key.
If you need to set up an SSH Key,
we recommend reading this document:
[Use SSH keys to communicate with GitLab](https://docs.gitlab.com/ee/ssh/index.html#add-an-ssh-key-to-your-gitlab-account)
.

![Adding Root SSH](https://res.cloudinary.com/fluid-attacks/image/upload/v1670942728/docs/web/groups/scope/ssh.png)

Remember to click on the
**Check Access** button
or validation if the credential
gives access to clone the repository.

### Adding a root with the Azure DevOps PAT

**Azure DevOps** is a platform that
provides software development services,
among those able to have repository
management and control the source code.
We invite you to access the official
documentation of
[Azure DevOps](https://learn.microsoft.com/en-us/azure/devops/user-guide/what-is-azure-devops?toc=%2Fazure%2Fdevops%2Fget-started%2Ftoc.json&view=azure-devops)
if you want more information.

![Adding Root azure](https://res.cloudinary.com/fluid-attacks/image/upload/v1670943031/docs/web/groups/scope/azure.png)

After entering these data,
click on **Check Access**.
If the information given is correct,
the Root will be created successfully.

:::note
Remember that you can also add
all this credentials types in
**Global Credential**.
For more information,
click [here](/tech/platform/organization/tech/platform/organization/credentials/).
:::

## Status in Git Root

The status help us to see how our
repository is in the cloning process.
We manage a total of six status.

- **Cloning:**
  The repository is being cloned.
- **Ok:**
  The cloning was successful.
- **Failed:**
  Something went wrong with the cloning.
- **N/A:**
  The root is inactive.
- **Unknown:**
  Is the initial state
  when creating a root,
  meaning it has not yet
  been cloned or is glued
  for this action.
- **Queued:** A queued machine
  run to check this root.

## Environments

Here you see the environments
according to the Git Roots
added to them.

## Environments table

In the environments table,
you can see the environments
added in Git Roots.

![Environments Table](https://res.cloudinary.com/fluid-attacks/image/upload/v1683039932/docs/web/groups/scope/env_url_table_new.png)

There is also a downward-facing
arrow on the left,
which,
upon click,
it shows you the creation date
and the Git Root corresponding
to that registered environment.

![Environment Registered](https://res.cloudinary.com/fluid-attacks/image/upload/v1659123650/docs/web/groups/scope/env_url_registered_new.png)

## Managing git root environments

Authorized users will also find the
**Environments** tab in the edit modal.
You can add environments corresponding
to the selected git Root by clicking
on the **Add Environment** button.

![Environment URLs Tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1673434992/docs/web/groups/scope/add_enviroment_new.png)

Here you will get a popup window
where you will have to select which
environment URL type you want to add,
which can be:
Mobile,
Cloud,
and Url.

- **Cloud:**
  You enter the credentials
  to access AWS,
  Azure,
  or Google Cloud platform.
- **Mobile:**
  You can add files with apk
  extension **(Android Package)**.
- **URL:**
  Here you enter the URL where
  you have deployed your application.

Remember that you can also delete
any environment by clicking on
the trash button.

![Delete Environment](https://res.cloudinary.com/fluid-attacks/image/upload/v1673436495/docs/web/groups/scope/trash_button_new.png)

:::note
You can also find in the Environment URLs
view how to add secrets.
Click [here](/tech/platform/groups/scope/roots#secrets)
if you want to know more.
:::

## Add secrets on AWS

Adding the **secrets/credentials**
of the AWS environment in the platform is very easy.
First,
select which Git Root we will add this to.

![Select Git Root](https://res.cloudinary.com/fluid-attacks/image/upload/v1685103494/docs/web/groups/scope/select_gitroot.png)

When you select it,
go to the second tab called **Environments.**
You can add this by choosing the type of environment;
in this case,
you will select **Cloud.**
You can enter
[here](/tech/platform/groups/scope/roots/#managing-git-root-environments)
if you want to know more about the other types of environments.

![Cloud option](https://res.cloudinary.com/fluid-attacks/image/upload/v1685103630/docs/web/groups/scope/cloud_option.png)

You will see a window called Cloud Name;
select the **AWS** option here.
Then you can fill in three fields:
**AWS account ID, AWS_ACCESS_KEY_ID,** and **AWS_SECRET_ACCESS_KEY.**

To obtain these values
you can check the section
[AWS Enrollment](/tech/platform/groups/scope/other-sections/aws-enrollment)

![AWS option](https://res.cloudinary.com/fluid-attacks/image/upload/v1685103903/docs/web/groups/scope/aws_option.png)

- **AWS account ID:** The ID that represents that AWS environment;
  note that it is made of at least twelve characters.

> **Note:** Just by having the account ID,
> you can confirm and register the environment,
> but remember that to have access to this infrastructure,
> you have to fill in the other two fields,
> which are the KEY.

- **AWS_ACCESS_KEY_ID:** The ID that represents the login
  key comprises alphanumeric characters.

- **AWS_SECRET_ACCESS_KEY:** The password to enter this environment
  is composed of alphanumeric characters.

Your credentials will be checked,
if they do not meet
the recommended characteristics here
[AWS Enrollment](/tech/platform/groups/scope/other-sections/aws-enrollment)
you will see a window
to confirm that you still want to add them,
remember that this can lead
to the CSPM module only running partially.

![Enviroment view](https://res.cloudinary.com/fluid-attacks/image/upload/v1687378854/docs/web/groups/scope/credentials_double_confirmation.png)

By filling out these fields,
you will be added to this environment,
which you can see in the Environments section.

![Enviroment view](https://res.cloudinary.com/fluid-attacks/image/upload/v1685104181/docs/web/groups/scope/enviroment_view.png)

Remember that you also can add the secrets of this table of environments.
To learn more about how to do it,
you can enter
[here.](tech/platform/groups/scope/roots/#secrets)

## IP roots

An IP address is the unique
identifier of a device on the
Internet or a local network.
When you provide us with an IP address,
we assess the security of all
web applications accessible
through this target.
If your [group](/tech/platform/groups/introduction/)
has [Black services,](/about/glossary/#black-box)
you will have **IP Roots** and **URL roots** in Scope section.

## IP roots table

The IP roots table gives us summary
information of the address you want to be analyzed.

![Scope IP root](https://res.cloudinary.com/fluid-attacks/image/upload/v1675252751/docs/web/groups/scope/ip_root.png)

You will find in this table the following information:

- **Address:**
  Your IP address to which you want to validate.
- **Nickname:**
  The identifier name of that IP.
- **State:**
  There are two states:
  **Active** and **Inactive**.
  Active means that the root is being tested
  and Inactive means that the root is no being tested.
  The same reasons are validated to deactivate
  a root IP as in a Git Root if you want
  to see more,
  click [here.](/tech/platform/groups/scope/roots/#deactivate-a-git-root)

## IP Roots functionalities

### Add new IP root

To add a new IP root,
you need to go to the Scope
section of the group of your
choice and click on **Add new root.**

![Scope IP root](https://res.cloudinary.com/fluid-attacks/image/upload/v1675249670/docs/web/groups/scope/scope_ip.png)

A pop-up window will appear,
asking you to enter the details
of the root (in this case,
IP address) you want to add.

![IP Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1657141769/docs/web/groups/scope/iproot_add_new.png)

Here are the definitions of
the details you need to enter:

- **Address:**
  IP address where the
  environment to be
  assessed is deployed.
- **Nickname:**
  An alternative name to
  easily identify the IP
  root in the future.

Once the IP address is added,
it will be listed below IP Roots.
There,
it is shown whether it is active.

![IP Roots activate](https://res.cloudinary.com/fluid-attacks/image/upload/v1675249990/docs/web/groups/scope/ip_activate.png)

### Edit a IP Root

You only have to click on the IP
root you want to edit.
A pop-up window will appear where
you can change the nickname.

![edit IP root](https://res.cloudinary.com/fluid-attacks/image/upload/v1675269101/docs/web/groups/scope/edit_ip_root.png)

### Deactivate a IP Root

Disabling a root IP handles the same
validations as disabling a Git root.
You can see this information by clicking
[here.](/tech/platform/groups/scope/roots/#deactivate-a-git-root)

## URL roots

URL roots are dynamic
environments that have already
been deployed to a web server.

## URL roots table

In this table,
you will find the following information.

![URL Roots table](https://res.cloudinary.com/fluid-attacks/image/upload/v1675269489/docs/web/groups/scope/url_root_table.png)

- **Host:**
  The domain name or IP address.
- **Path:**
  The path that will give to validate the URL.
- **Port:**
  The port number that helps us to give
  access to the URL.
- **Protocol:**
  The protocol is using the browser.
- **Query:**
  The query component serves to identify
  a resource within the scope of the
  URI's scheme.
- **Nickname:**
  The identifier name of that URL.
- **State:**
  There are two states: **Active** and **Inactive**.
  The same reasons are validated to
  deactivate a root IP as in a Git Root
  if you want to see more,
  click [here.](/tech/platform/groups/scope/roots/#deactivate-a-git-root)

## URL roots functionalities

### Add new URL root

To add a new URL root,
go to the Scope section of the
group of your choice and click
on the Add new root button.

![URL Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1675250254/docs/web/groups/scope/url_scope.png)

The following pop-up window will appear,
asking you to enter the details
of the URL  you want to add.

![Add URL Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1675327909/docs/web/groups/scope/add_new_url.png)

The details you need to enter
are defined as follows:

- **URL:**
  Address where the
  environment is deployed.
- **Nickname:**
  An alternative name to
  easily identify the URL
  root in the future.

The URL roots you add will be
listed below **URL Roots**.
There,
it is shown whether it is active.

![Add URL Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1675328694/docs/web/groups/scope/activate_url_root.png)

### Edit a URL Root

By clicking on the URL of your interest,
you will be able to edit the nickname of the URL.

![Edit URL Roots](https://res.cloudinary.com/fluid-attacks/image/upload/v1675282250/docs/web/groups/scope/url_edit.png)

If you notice,
you can also add or edit the secrets of that URL.
For more information about this,
click [here.](/tech/platform/groups/scope/roots/#secrets)

### Deactivate a URL Root

Disabling a root URL handles the same validations
as disabling a Git an IP root.
You can see this information by clicking
[here.](/tech/platform/groups/scope/roots/#deactivate-a-git-root)

## Single root assessment

We assess only one
repository branch per group,
looking for vulnerabilities in
one single version of the system.
Testing only one branch allows
us to do a coherent assessment
and makes it easier to keep a
track of findings and fixes.
Therefore,
your development team can
efficiently manage the
reported vulnerabilities,
and our team can efficiently
verify the effectiveness of
the fixes you implemented.

> **Note:** We also tested the equivalent
> environment to the provided code branch,
> which means one environment.

## Secrets

This section allows
you to see,
add,
edit and delete secrets.
These are usernames,
passwords,
email addresses,
tokens,
etc.,
that give us access to
private repositories
and environments.
As this is sensitive information
that has to be protected,
only a limited group of
people has access to it.
The management of secrets
is done for previously
created roots or URLs,
listed in the tables **Git Roots,**
**Environment URLs** or **URL Roots**
in the Scope section.

![Go to Secrets Section](https://res.cloudinary.com/fluid-attacks/image/upload/v1671801491/docs/web/groups/scope/ways_add_secrest_new.png)

You can select a
root from Git Roots.
You will immediately see a
pop-up window with three tabs,
the third one being **Secrets**.

![Secrets Window](https://res.cloudinary.com/fluid-attacks/image/upload/v1671801585/docs/web/groups/scope/secrets_tab_new.png)

To add a new secret,
you have to access the Secrets
section and click on the
**Add secret** button.

![Add Secret Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1652717752/docs/web/groups/scope/secrets_click_add_new.png)

The secret must consist
of key and value.
Additionally,
you can include a short description.

![Add Secrets](https://res.cloudinary.com/fluid-attacks/image/upload/v1671801635/docs/web/groups/scope/add_secret.png)

When you click Confirm,
the secret is made accessible
to our hackers on Fluid Attacks' platform.
You can also delete or edit
all the secrets you add by
clicking on the
corresponding button.

![Secret Details](https://res.cloudinary.com/fluid-attacks/image/upload/v1671802063/docs/web/groups/scope/edit_secret_new.png)

From Environment URLs and URL Roots
you have to select the URL
where you want to add,
delete or edit secrets and
follow the same procedure
described above.

## Existing credentials

Credentials help us to have
access to one or multiple
repositories.
When creating or
editing a root,
you can see the
**Existing credentials** field.
Clicking on it will display a
list of credentials previously
used for other repositories.

![Existing Credentials Field](https://res.cloudinary.com/fluid-attacks/image/upload/v1671803954/docs/web/groups/scope/existing_credentials.png)

If any of the credentials in
the list is useful for the root
that you want to create or edit,
select it,
and the **Credential type** and
**Credential name** fields will
be autofilled.

![Credentials Type](https://res.cloudinary.com/fluid-attacks/image/upload/v1671804125/docs/web/groups/scope/activation.png)

> **Note:** The credentials you create individually in
> Scope or the Global Credentials tab will be saved
> at the organization level,
> meaning they are available in all the groups that
> make up the organization.

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
