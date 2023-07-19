---
id: reporting-vulns
title: Reporting in existing types of vulnerabilities
sidebar_label: Reporting in existing types of vulnerabilities
slug: /tech/analysts/reporting-vulns
---

The `Fluid Attacks` platform has the
necessary tools to be able to
report all the vulnerabilities
encountered in the group's scope.
In order to access this functionality,
you can go to the main screen
for the specific type of
vulnerability you want to report.

When you get there you will
see three different buttons
at the bottom of the table.

![Report](https://res.cloudinary.com/fluid-attacks/image/upload/v1661973578/docs/web/vulnerabilities/reporting-vulns/reporttab.png)

The first button
**Download Vulnerabilities** gives
you a `.yaml` file describing all
the vulnerabilities of this type.
Second button “Explore” is the one
you use to search on your device
the `.yaml` vulnerabilities file.
Lastly the **Update Vulnerabilities**
button is used after you select
said file and want to upload
its vulnerabilities.

## The format to report vulnerabilities

The `.yaml` file mentioned before
needs to have a specific format
or it will give you an error.
You can report vulnerabilities
present in the code of a repository
or directly in the application
that results from this code,
in order to do this you can
write a section in the `.yaml`
file starting with
**inputs**, **lines** or **ports**.

The following is an example for
this reporting `.yaml` file:

```yaml title="vulnerabilites_to_update.yaml"
inputs:
  - field: "HTTP:GET:REQUEST:BODY:password"
    url: https://example.com
    state: open
    repo_nickname: universe
    stream: home,login
    source: analyst
    tool:
      impact: direct
      name: Burpsuite
    cvss_v3: CVSS:3.1/AV:N/AC:H/PR:H/UI:N/S:C/C:H/I:H/A:H
    cwe_ids:
      - CWE-1035
      - CWE-770
      - CWE-937
    tags:
      - qa
      - frontend
lines:
  - commit_hash: 5b5c92105b5c92105b5c92105b5c92105b5c9210
    line: 123,45-88
    path: path/to/file1.ext
    state: open
    repo_nickname: universe
    source: analyst
    tool:
      impact: direct
      name: none
    tags:
      - infra
      - backend
ports:
  - host: 192.168.1.44
    port: "4444"
    state: open
    repo_nickname: universe
    source: analyst
    tool:
      impact: direct
      name: tool-1
    cvss_v3: "CVSS:3.1/MA:X/AC:L/UI:N/S:U/C:H/I:N/A:N/E:H/RL:U/RC:C/AV:A/PR:L"
    cwe_ids:
      - "CWE-122"
      - "CWE-787"
```

You can add as many
vulnerabilities as you need,
you just have to separate
each one with a hyphen and
add the necessary fields.

Some fields are valid to
all sections, as others are
specific to each one.
The fields present on all
sections are:

- **Source (Required):**
  Where the origin of the
  location was given.
  Which can be
  **analyst**,
  **customer**,
  **deterministic**,
  **escape**
  or **machine**.
- **State (Required):**
  This field specifies if the
  vulnerability currently still
  persists or if it has already
  been resolved.
  It can be
  **open**,
  **closed**,
  **rejected**
  or **submitted**.
- **Tool (Required):**
  It will give us information
  on which tool the
  vulnerability was found.
  This field is divided into
  two fields: **Impact**;
  here,
  you specify if it was direct
  or indirect and **name** you
  specify the tool's name.
  Keep in mind that you
  can put several tools.
- **Repo_nickname (Required):**
  This is the nickname that
  a group administrator gives
  to a specific repository.
  You can find it in the
  **Scope** tab of the group
  in the downward-facing arrow
  on the left of the
  **Type** column,
  which,
  upon click,
  will unfold the description
  for each repository and you
  will see de **Nickname**,
  as seen in the following image.

  ![Inputs Format Nickname](https://res.cloudinary.com/fluid-attacks/image/upload/v1661973578/docs/web/vulnerabilities/reporting-vulns/format_report_nickname.png)

  You can also use the GraphQL API
  to find the nickname by using this query:

  ```graphql
  query {
    group(groupName: "your group name") {
      name
      roots {
        ... on GitRoot {
          environment
          nickname
        }
        ... on IPRoot {
          address
          nickname
          state

        }
        ... on URLRoot {
          host
          nickname
          path
        }
      }
    }
  }
  ```

  You can go to this [link](/tech/api)
  in order to learn more about using the
  GraphQL API to access all of the
  information in the Fluid Attacks' platform.
- **Cvss_v3 (Optional):**
  You can assign or update the CVSS v3.1
  severity score directly to each
  vulnerability by using this field.
  It takes the severity vector as defined
  by the CVSS specification and it can
  be obtained with the help
  of the CVSS calculator [here][CVSS_CALCULATOR].
- **Cwe_ids (Optional):**
  This is a list of the
  [Common Weakness Enumeration (**CWE**)][CWE_LIST]
  ids that are related directly
  to this vulnerability.
  Each item must comply with
  the format `CWE-<id_number>`
  as shown in the example.
- **Tags (Optional):**
  Through this field you can
  assign the labels or tags
  later displayed in the **Tags**
  column of the location's table.

### The inputs yaml format

This is the structure of the
**inputs** that you have to fill in.
Here we explain what each field refers to.

```yaml
inputs:
  - field: "HTTP:GET:REQUEST:BODY:password"
    url: https://example.com
    state: open
    repo_nickname: universe
    stream: home,login
    source: analyst
    tool:
      impact: direct
      name: Burpsuite
```

- **Field (Optional):**
  The name of the specific
  field or fields in the
  application that enables
  the vulnerability.
- **Url (Required):**
  This is the web address in
  which we can find the field
  that has the vulnerability.
- **Stream (Required):**
  This information is very important
  for future analysts that access
  the group to be able to find
  the vulnerability.
  You must write a breadcrumb trail
  that starts at the page that is
  viewed first when accessing the
  environment url (e.g. Home,
  Login,
  Dashboard) and write each link
  name or functionality you have
  to access in order to be able
  to reach the field that
  has the vulnerability.

### The lines yaml format

Then,
we also have the format for
reporting **line** vulnerabilities:

```yaml
lines:
  - commit_hash: 5b5c92105b5c92105b5c92105b5c92105b5c9210
    line: 123,45-88
    path: path/to/file1.ext
    state: open
    repo_nickname: universe
    source: analyst
    tool:
      impact: direct
      name: none
```

- **Line (Required):**
  This is the specific line or
  lines in the file that contains
  the type of vulnerability
  that is being reported.
- **Commit_hash (Required):**
  This is a 40 characters long
  string that points to the
  specific commit that last
  modified the file before
  encountering the vulnerability.
- **Path (Required):**
  This is the directory path
  to find the file inside
  its repository.

### The ports yaml format

Related to the format for
reporting **port** vulnerabilities:

```yaml
ports:
  - host: 192.168.1.44
    port: "4444"
    state: open
    repo_nickname: universe
    source: analyst
    tool:
      impact: direct
      name: tool-1
```

- **Host (Required):**
  This is the URL from which the
  specific port will be reported.
- **Port (Required):**
  This is a string containing the
  specific port number.

[CVSS_CALCULATOR]: https://www.first.org/cvss/calculator/3.1
[CWE_LIST]: https://cwe.mitre.org/data/index.html
