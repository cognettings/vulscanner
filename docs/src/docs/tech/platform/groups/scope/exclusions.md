---
id: exclusions
title: Exclusions
sidebar_label: Exclusions
slug: /tech/platform/groups/scope/exclusions
---

There are cases
when it is necessary
to exclude a number of files
or whole folders
from the
[scope](/tech/platform/groups/scope/roots/)
of the tests we perform.
There are many reasons
why you may want to do this,
maybe you want to exclude
the many functional tests
that your repository has,
exclude some dummy files
that you haven't deleted,
etc.,
the circumstances are varied.
[Fluid Attacks' platform](/tech/platform/introduction)
gives you a way to do this,
however,
remember that any files or folders
excluded by the gitignore
will prevent any more vulnerabilities
from being reported for them
and are effectively taken out
of the scope of the group,
so we advice you
to be careful with this.

> **Note:** There is no limit on exclusions;
> you can add as many as necessary according to your requirements.

## How to exclude paths from the scope of my group?

In order to do this,
we have a section
that appears
when you are adding or editing
a git root in your group.

![Git Root Buttons](https://res.cloudinary.com/fluid-attacks/image/upload/v1682973987/docs/web/groups/scope/add_button.png)

You just need to go
to the scope section of your group
and click on the **Add new root**
or select the already created root
you want to add that exclusion.
Depending on what you want to do,
and a window will show up.

There you can see
the question
**Are there files in your selection that you want the scans to ignore?**,
If you click **YES,**
you will get a warning as a preventive message,
followed by the field you can start adding patterns
for the files and/or folders you want to exclude.
In this way you can specify
the paths that you don't want us to test.
If you need to add more,
click on the **Add another** button.

![Exclusions button](https://res.cloudinary.com/fluid-attacks/image/upload/v1668475380/docs/web/groups/scope/exc_isopns_button.png)

For your convenience,
you can also click
[this link](https://mirrors.edge.kernel.org/pub/software/scm/git/docs/gitignore.html#_pattern_format)
to access said web page.
Using these **patterns**
you can efficiently exclude
all the files and folders you want,
however,
we advice you to be careful
when you use the **wildcard(*)**,
as this may cause you to accidentally exclude
something you don't want to
and stop receiving reports
of any vulnerabilities in it,
so whenever you can,
always try to be specific
when excluding paths.

## Examples

Here we have some examples:

- node_modules/
- build/tmp/
- test/*.js (Here we use the wildcard that we advised you to be careful with)
- repo-root/dummy/excludeme.js

> **Note:** This subsection is pending review.
> Some of the information might be outdated.

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
