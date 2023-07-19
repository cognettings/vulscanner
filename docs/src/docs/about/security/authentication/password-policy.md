---
id: password-policies
title: Password Policies
sidebar_label: Password Policies
slug: /about/security/authentication/password-policies
---

## Objective

The objective of this document is to reflect the measures and configurations
implemented to comply with the password policy established by `Fluid Attacks`.
These measures are intended to ensure the strength and protection of passwords
used in the system, following recommended security best practices.

## Description

The internal password management policy at `Fluid Attacks` has been established to
guarantee the security and protection of the organization's data and systems.
Below are the specifications and configurations implemented:

- **Minimum password length:** Passwords must have a minimum length of 16
  characters to increase complexity and resistance to brute force attacks.

- **Character requirements:** Passwords are required to contain at least 1
  lowercase character, 1 uppercase character, 1 numeric character, and 1
  special character. This helps diversify the elements that can be part of
  a password.

- **Password lifetime:** A minimum password lifetime of 120 minutes and a maximum
  password lifetime of 30 days are established. This means users must change
  their passwords at least every 30 days, and passwords will automatically
  expire after 30 days.

- **Password expiration notification:** Users will receive a notification 5
  days before their password expires, reminding them to change it.

- **Password history count:** A history of the previous 24 passwords is recorded
  to prevent the reuse of recent passwords.

- **Account locking after failed attempts:** After 10 failed attempts, the user's
  account will be automatically locked to prevent brute force attacks.

- **Automatic unlock time:** After a lockout, the account will automatically
  unlock after 10 minutes.

- **Secure password verification:** Passwords are checked to ensure they do not
  contain the username, first and last name, or common words to avoid the use of
  predictable passwords.

- **Password recovery:** Password recovery is enabled through email and recovery
  questions to assist users in resetting their passwords in case of forgetting.

- **Account lockout notification:** Users will be notified by email if their
  account is locked due to failed attempts.

- **Email recovery token lifetime:** The token sent for password recovery
  via email will expire after 60 minutes to ensure security.

## Configuration

In this section, we detail the configurations implemented to comply with the
password policy established by `Fluid Attacks`. These configurations aim to
ensure the strength and protection of passwords used in the system,
following recommended security best practices.

![Okta Password Configuration](https://res.cloudinary.com/fluid-attacks/image/upload/v1688685746/docs/about/security/authentication/oktapolicy.png)

[Password Configuration](https://gitlab.com/fluidattacks/universe/-/blob/trunk/common/okta/infra/settings.tf#L16)
in the Terraform file and
[Terraform reference](https://registry.terraform.io/providers/okta/okta/latest/docs/resources/policy_password_default)
for further documentation.

With these implemented measures, we aim to ensure the strength and protection
of passwords used in the system, following the recommended security best
practices by `Fluid Attacks`.

## Requirements

- [129. Validate previous passwords](/criteria/requirements/129)
- [130. Limit password lifespan](/criteria/requirements/130)
- [226. Avoid account lockouts](/criteria/requirements/226)
