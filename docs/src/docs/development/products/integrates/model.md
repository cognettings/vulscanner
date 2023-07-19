---
id: model
title: Data Model
sidebar_label: Data Model
slug: /development/products/integrates/model
---

In our platform,
various statuses are managed for both
users and internal roles.
Below is a comprehensive list of these
statuses along with their definitions.

**Vulnerability State Status:**
This section manages the statuses
the Vulnerability view,
which are classified as follows:

- **SUBMITTED:** When the Hacker role reports a vulnerability,
  it enters the "SUBMITTED" status,
  awaiting approval or rejection.
  **(Internal flow status)**

- **REJECTED:** If the Reviewer role determines the
  reported vulnerability in the "SUBMITTED" status,
  decide if it is "VULNERABLE" or not,
  and it will be marked as "REJECTED."
  **(Internal flow status)**

- **VULNERABLE:** State of a vulnerability for which
  a fix has not yet been applied. **(User flow status)**

- **SAFE:** State of a vulnerability for which
  a solution has already been applied and
  corroborated in a re-attack while being safe.
  Also,
  a vulnerability can be marked as safe due to
  an exclusion when users deactivate roots
  (taking a repository out of the scope)
  **(User flow status).**

- **DELETED:** This status is if the reported
  vulnerability needs to be eliminated by False Positive,
  misreporting,
  or accident. **(Internal flow status)**

- **MASKED:** When the service is terminated,
  and the group is deleted,
  all vulnerabilities are archived without details,
  but we are left with evidence for analytics
  that it existed at some point. **(Internal flow status)**

**Vulnerability Treatment Status:**
This section manages the statuses the Treatment,
which are classified as follows:

- **UNTREATED:** Initial state with a vulnerability,
  i.e.,
  without treatment **(User flow status).**

- **IN PROGRESS:** When the vulnerability is assigned
  to a team member for its solution,
  it remains in this state **(User flow status).**

- **ACCEPTED:** When the vulnerability is permanently
  or temporarily accepted **(User flow status).**

- **ACCEPTED UNDEFINED:** When the user decides to live
  with the vulnerability **(User flow status).**

**Vulnerability Zero Risks Status:**
This section manages the statuses the Zero Risk,
which are classified as follows:

- **REQUESTED:** The user requests the application
  of Zero Risk to the vulnerability,
  accepting that it does not represent a risk for them
  as they have additional means of mitigation
  **(User flow status).**

- **CONFIRMED:** If we confirm that it does not represent a risk
  given their means of mitigation **(User flow status).**

- **REJECTED:** If not approved to be marked as Zero Risk
  **(User flow status).**

**Vulnerability Verification Status:**
This section manages the statuses the reattacks,
which are classified as follows:

- **Requested:** When the client has tested a solution
  to the vulnerability,
  it requests the validation of this by sending an initiating reattack,
  leaving the vulnerability in this state **(User flow status).**

- **ON HOLD:** If an open eventuality prevents verifying
  the solution provided by the user,
  it enters this state until the eventuality is solved
  **(User flow status).**

- **VERIFIED:** It has two states: **VULNERABLE**
  if the applied solution is not effective or **SAFE**
  if it is effective and the vulnerability is no
  longer a threat **(User flow status).**

**Vulnerability Acceptance Status:**
This section manages the statuses when you want
to apply for permanent treatment accepted,
which are classified as follows:

- **SUBMITTED:** The user requests the application of permanent
  acceptance of a vulnerability **(User flow status).**

- **APPROVED:** When the approval of this treatment is given,
  the vulnerability enters this approval state **(User flow status).**

- **REJECTED:** When the approval of this treatment is
  not given **(User flow status).**
