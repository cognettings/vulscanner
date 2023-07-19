---
id: vulnerabilities
title: Vulnerabilities
sidebar_label: Vulnerabilities
slug: /tech/platform/groups/vulnerabilities
---

The **Vulnerabilities** section is
the first one you see when clicking
on one of your group's names.

Note that if you keep the mouse cursor
on the tab vulnerabilities,
you can see the total of all open vulnerabilities in that group.

![Total of vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1677560179/docs/web/groups/vulnerabilities/total.png)

## Vulnerabilities Table

In the Vulnerabilities section,
you will find a table containing
all the [types of vulnerabilities](/criteria/vulnerabilities/)
reported in the selected
[group.](/tech/platform/groups/group-view)
This table includes different columns,
which you can activate or deactivate
according to the information you want
to see using the [columns filter](/tech/platform/groups/vulnerabilities/#columns-filter)
button.

![Vulnerability Table First Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1675162266/docs/web/groups/vulnerabilities/vulnerabilities.png)

In total,
we have twelve columns which are
described below:

- **Type:** The name of the
  type of vulnerability from
  our [standardized set](/criteria/vulnerabilities/)
  whose characteristics are met by
  the vulnerability found in
  your system.
- **Status:** The condition of
  the type of vulnerability,
  which is **Vulnerable** if at least
  one vulnerability has not
  yet been remediated;
  otherwise,
  it is **Safe.**
- **Severity:** The maximum
  [CVSS v3.1 (Common Vulnerability Scoring System)](/about/glossary#cvss)
  temporal score among the open vulnerabilities
  in this type of vulnerability.
- **% Risk Exposure:**
  Represents the contribution that this type of vulnerability
  is making to the metric [CVSSF](/about/glossary#cvssf)
  for this group.
  It is given as a percentage and only open vulnerabilities
  are taking into account.
- **Open vulnerabilities:**
  The total number of locations where
  the type of vulnerability
  was found and is still
  vulnerable; that is,
  not yet remediated.
- **Last report:** The number
  of days elapsed since
  we found a vulnerability
  of that specific type,
  regardless of its vulnerable
  or safe status.
- **Age:** The number of days
  elapsed since the type of
  vulnerability was found in
  your system for the first
  time.
- **Remediation %:**
  The percentage of closed
  vulnerabilities of that type.
- **Reattack:** The status of
  the
  [reattacks](/tech/platform/reattacks/) for the type
  of vulnerability,
  which is **Pending** if at least
  one requested reattack is
  due to one of the vulnerabilities
  of this type; otherwise,
  it is just a hyphen.
- **Release Date:**
  Date when the typology was reported.
- **Treatment:**
  List the
  [treatments](/tech/platform/vulnerabilities/management/treatments) that this
  typology has.
- **Description:**
  A definition of the type of
  vulnerability.

Note that you can identify when a vulnerability type is new
because you will see the tag called **new.**
Remember that this tag will be enabled for eight days.
After these days,
it will disappear.

![new tag](https://res.cloudinary.com/fluid-attacks/image/upload/v1677668727/docs/web/groups/vulnerabilities/newtag.png)

There is also a downward-facing
arrow on the left of the Type column,
which,
upon click,
you will find the information that
the column filter offers you.

![Vulnerability Table Second Half](https://res.cloudinary.com/fluid-attacks/image/upload/v1675162531/docs/web/groups/vulnerabilities/down_row.png)

## Vulnerabilities type

In the vulnerability view,
you can visualize the different
[typologies](/criteria/vulnerabilities/)
of reported vulnerabilities.
These typologies can be repeated several times,
grouping within these vulnerabilities
[(locations)](/tech/platform/vulnerabilities/management/locations)
with the same characteristics such as
[description,](/tech/platform/vulnerabilities/management/description)
recommendation,
[severity](/tech/platform/vulnerabilities/severity)
and other characteristics.
For more information on the location section,
click [here](/tech/platform/vulnerabilities/management/locations/).

![Vuln type](https://res.cloudinary.com/fluid-attacks/image/upload/v1681343608/docs/web/groups/vulnerabilities/vuln_type.png)

## Functionalities

In the Vulnerabilities section,
you can see the following functionalities:

- [Columns filter](/tech/platform/groups/vulnerabilities#columns-filter)
- [Filters](/tech/platform/groups/vulnerabilities#filters)
- [Generate report](/tech/platform/groups/reports)
- [Search bar](/tech/platform/groups/vulnerabilities#search-bar)

### Columns filter

One way of filtering the
table is by hiding or
showing columns.
To do this,
you need to click the
**Columns button.**

![Columns button](https://res.cloudinary.com/fluid-attacks/image/upload/v1682607222/docs/web/groups/vulnerabilities/filter_column.png)

This will cause a pop-up
window to appear,
from which you can enable
and disable columns.

![Filtering Columns](https://res.cloudinary.com/fluid-attacks/image/upload/v1673907259/docs/web/groups/vulnerabilities/columns_filter.png)

### Filters

The other way of filtering is
by clicking the **Filters button**.
Here you will have the activated
filters that you have at the same
time activated in the column filter.

![Filters Button](https://res.cloudinary.com/fluid-attacks/image/upload/v1675162726/docs/web/groups/vulnerabilities/filters.png)

Remember that you can see the filters you
have applied in the table.

![Filters applied](https://res.cloudinary.com/fluid-attacks/image/upload/v1675164134/docs/web/groups/vulnerabilities/filters_aplied.png)

> **Note:** These applied filters will be
> kept in the vulnerability view in the
> different groups of the same or another organization.

### Search bar

The search bar filters the information
contained in the columns of the table.

:::note
You can also find in the vulnerability
view how to generate reports.
Click [**here**](/tech/platform/groups/reports)
if you want to know more.
:::
