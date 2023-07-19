---
id: okta
title: Okta
sidebar_label: Okta
slug: /development/stack/okta
---

## Rationale

[Okta][OKTA]
is the
[IAM](https://en.wikipedia.org/wiki/Identity_management)
platform we use for managing
access to hundreds of applications
used across our company.
It allows us to give
access to applications
without disclosing credentials
and maintaining a
[least privilege](/criteria/requirements/186)
approach.

The main reasons why we chose
it over other alternatives are:

1. It is [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service),
    allowing us to forget about maintaining
    the infrastructure it relies on.
1. Being a
    [SSO](https://en.wikipedia.org/wiki/Single_sign-on)
    platform,
    talent only need to remember their
    [Okta][OKTA] password.
    Everything else can be accessed
    once they're inside.
1. It provides a
    [universal directory](https://www.okta.com/products/universal-directory/)
    that allows us to have
    users, departments,
    applications and permissions
    in a single place.
1. It supports
    [Multi-factor authentication][MFA]
    by using
    [OTP's](https://en.wikipedia.org/wiki/One-time_password)
    that regenerate every thirty seconds
    and [Push notifications](https://en.wikipedia.org/wiki/Push_technology)
    through its
    [Okta Verify app](https://www.okta.com/integrations/okta-verify/)
    on both
    [IOS](https://en.wikipedia.org/wiki/IOS)
    and
    [Android](https://en.wikipedia.org/wiki/Android_(operating_system)).
1. As
    [Multi-factor authentication][MFA]
    can be done on the user's phone,
    we do not need to manage independent
    [security tokens](https://en.wikipedia.org/wiki/Security_token).
1. Its
    [Multi-factor authentication][MFA]
    uses
    [OOBA](https://doubleoctopus.com/security-wiki/authentication/out-of-band-authentication/),
    a state of the art authentication process
    that uses two different communication channels,
    one for the application itself
    and a separate one for the verification method.
    Such process reduces the chances of identity theft,
    as both channels would need to be compromised by an attacker.
1. It enforces
    [Biometric MFA](https://www.okta.com/identity-101/biometrics-secure-authentication/)
    for both face and fingerprint
    if the device supports it.
1. It supports
    [serverless automatic provisioning](https://help.okta.com/en/prod/Content/Topics/Apps/Provisioning_Deprovisioning_Overview.htm),
    allowing us to keep
    other directories
    from services like
    [Google Workspace](https://workspace.google.com/) and
    [AWS IAM](/development/stack/aws/iam/)
    automatically synchronized
    without additional effort.
1. It supports
    [SAML](https://en.wikipedia.org/wiki/Security_Assertion_Markup_Language) and
    [OAuth](https://en.wikipedia.org/wiki/OAuth),
    allowing us to give users
    access to applications
    without having to manage credentials.
1. It supports
    [thousands](https://www.okta.com/integrations/)
    of preconfigured integrations.
1. It provides
    [in-depth reports and logging](https://www.okta.com/reporting/)
    regarding security and overall user usage.
1. It provides a
    [RADIUS agent](https://help.okta.com/en/prod/Content/Topics/integrations/ha-main.htm)
    for authenticating
    on external infrastructure like
    [VPN's](https://en.wikipedia.org/wiki/Virtual_private_network).
1. It allows
    [strong password](https://help.okta.com/en/prod/Content/Topics/Security/healthinsight/strong-passwords.htm)
    enforcement.
1. It can be
    [managed](https://registry.terraform.io/providers/okta/okta/latest)
    using [Terraform](/development/stack/terraform).

## Alternatives

1. [OneLogin](https://www.onelogin.com/):
    We used it for three years.
    It did not support
    as many integrations.
    It's automatic provisioning
    was not as flexible.
1. [Duo](https://duo.com/):
    It did not support
    as many integrations.
    It's automatic provisioning
    was not as flexible.

## Usage

We use [Okta][OKTA] for:

1. [Managing apps, groups, users and permissions](https://gitlab.com/fluidattacks/universe/-/blob/6e16ae7ed5a28d5f56601357a299eea18b20e283/makes/applications/makes/okta/src/terraform/data.yaml).
1. [Managing AWS roles with SAML](https://gitlab.com/fluidattacks/universe/-/blob/6e16ae7ed5a28d5f56601357a299eea18b20e283/makes/applications/makes/okta/src/terraform/aws-roles.tf).

We do not use [Okta][OKTA] for:

1. [Managing users via universal directory](https://www.okta.com/products/universal-directory/):
    We are [currently returning from JumpCloud](https://gitlab.com/fluidattacks/universe/-/issues/4561).
1. [Managing RADIUS](https://help.okta.com/en/prod/Content/Topics/integrations/ha-main.htm):
    The [Okta RADIUS Agent](https://help.okta.com/en/prod/Content/Topics/integrations/getting-started-about-radius.htm)
    only supports
    [PAP](https://pleasantsolutions.com/info/pleasant-password-server/j-user-administration/two-factor-authentication/setting-up-radius/radius-authentication-protocols)
    as authentication protocol,
    being the reason
    why we decided to
    look for other
    [RADIUS](https://en.wikipedia.org/wiki/RADIUS)
    providers once
    [returning from JumpCloud](https://gitlab.com/fluidattacks/universe/-/issues/4561)
    is finished.

## Guidelines

1. You can access [Okta][OKTA]
    by clicking [here](https://fluidattacks.okta.com/).
1. Any changes to
    [Okta][OKTA]
    infrastructure must be done via
    [Merge Requests](https://docs.gitlab.com/ee/user/project/merge_requests/)
    modifying its
    [Terraform module](https://gitlab.com/fluidattacks/universe/-/blob/6e16ae7ed5a28d5f56601357a299eea18b20e283/makes/applications/makes/okta/src/terraform).
1. To learn how to test and apply infrastructure via [Terraform](/development/stack/terraform),
    visit the
    [Terraform Guidelines](/development/stack/terraform#guidelines).

[OKTA]: https://www.okta.com/
[MFA]: https://www.okta.com/products/adaptive-multi-factor-authentication/
