---
id: aws-enrollment
title: AWS Enrollment
sidebar_label: AWS Enrollment
slug: /tech/platform/groups/scope/other-sections/aws-enrollment
---

Here you can find
all the information required by
a customer to enroll
an AWS cloud account to start
using the CSPM DAST module.

You will need three credentials
to use the AWS CSPM DAST module.

- AWS account ID
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY

You can check the way
to add this credential
to Fluid Attacks' platform here:
[AWS credentials](/tech/platform/groups/scope/roots#add-secrets-on-aws)

Now we will show you
how to get these credentials
from the AWS user interface.

We need to start session
in the AWS management console
with an user account authorized
to perform new user and access keys creation.

## AWS account ID

First of all,
click on the drop-down menu
where the name of the session is indicated.

![Session drop down menu](https://res.cloudinary.com/fluid-attacks/image/upload/v1685136610/docs/web/groups/scope/aws_console_view.png)

In this menu
you'll see a tag
with the name ***Account ID***,
this ID corresponds to the **AWS account ID**
for that environment
and it has 12 digits;
copy the ID without the dash symbols "-".

![AWS console view](https://res.cloudinary.com/fluid-attacks/image/upload/v1685136621/docs/web/groups/scope/session_drop_down_menu.png)

## AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY

We will need to generate
a pair of access keys for the account;
To create this pair
we will need a new user
and limit the permissions for that user,
we will do this through a group

To create a new user
we will go to Identity and Access Management (IAM)
and select the user section

![IAM user section](https://res.cloudinary.com/fluid-attacks/image/upload/v1685379562/docs/web/groups/scope/iam_user_section.png)

Click on the Add User button

![Add user button](https://res.cloudinary.com/fluid-attacks/image/upload/v1685382258/docs/web/groups/scope/add_user_button.png)

Add a name for the new user,
click next and create user.

![Add new user](https://res.cloudinary.com/fluid-attacks/image/upload/v1685383708/docs/web/groups/scope/add_new_user.png)

Then we proceed to create a new group
we will select the **User groups** section
and click on the **Create group** button.

![IAM user group section](https://res.cloudinary.com/fluid-attacks/image/upload/v1685386128/docs/web/groups/scope/create_group_button.png)

After that,
name the new group
and select the previously
created user

![Attach user](https://res.cloudinary.com/fluid-attacks/image/upload/v1685389381/docs/web/groups/scope/attach_user.png)

an attach the policy **ReadOnlyAccess**
that will give only read access
to all user inside this group.

![Attach permissions](https://res.cloudinary.com/fluid-attacks/image/upload/v1685386348/docs/web/groups/scope/attach_permssions.png)

Now we will to proceed
to create the access key pair,
select the **user** section,
find and select the previously created user.

![Find new user](https://res.cloudinary.com/fluid-attacks/image/upload/v1685392752/docs/web/groups/scope/find_new_user.png)

Now click on the **Security credentials** tab.

![Security credentials tab](https://res.cloudinary.com/fluid-attacks/image/upload/v1685393451/docs/web/groups/scope/security_credentials_tab.png)

Look for the **Access keys** section
and click the **Create access key** button.

![New access key button](https://res.cloudinary.com/fluid-attacks/image/upload/v1685394018/docs/web/groups/scope/new_access_key_button.png)

Select the options marked
on the following image.

![Access key settings](https://res.cloudinary.com/fluid-attacks/image/upload/v1685394689/docs/web/groups/scope/access_key_settings.png)

Click on next and
add a description
for the access key pair
and click the **Create access key** button.

![Access key description](https://res.cloudinary.com/fluid-attacks/image/upload/v1685395441/docs/web/groups/scope/access_key_description.png)

Now that we get the pair of secrets
copy them or download the .csv file,
remember don't keep your secrets
on text files

![Key pair](https://res.cloudinary.com/fluid-attacks/image/upload/v1685395998/docs/web/groups/scope/key_pair.png)
