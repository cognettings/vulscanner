---
id: vs-code
title: VS Code extension
sidebar_label: VS Code extension
slug: /talent/hacking/analysts/vs-code
---

The usability of the **Fluid Attacks**
extension in VS Code will help you in your
daily work in vulnerability reporting.
You need to have access to the group and
the repositories you are in charge of as an analyst.

First,
remember to download the extension
and perform the proper setup;
if you have doubts,
you can enter
[here.](/tech/ide/#download-extension)

Once the extension is ready,
enter the VS Code editor and open the terminal
path to the folder where you manage
all the projects in charge,
named **groups.**

When you open the folder,
you will see in the left bar a feature called
**groups manager.**

![groups manager](https://res.cloudinary.com/fluid-attacks/image/upload/v1688563364/docs/analysts/vs-code/extension.png)

When you click on **groups manager**,
it will list the folders of the projects
you are in charge of;
now,
if you see that some are missing,
you can manually add them,
as explained in this
[link.](/tech/ide/#troubleshooting)

Once you have the list of projects,
you can click on one of your interests,
and it will show you the repositories that compose it.

![Repositories](https://res.cloudinary.com/fluid-attacks/image/upload/v1688563431/docs/analysts/vs-code/repositories.png)

Right-clicking on any of these will give you three options:

- Attacked Lines: Lines that are already attacked.
- Clone Git Root: Start cloning the roots with
  that repository (Download the code).
- Environment URLs: URLs to attack.

![options](https://res.cloudinary.com/fluid-attacks/image/upload/v1688563472/docs/analysts/vs-code/options.png)

What we have to start is to clone the repositories,
then you must click on the second option **Clone Git Root.**
Remember that if the repositories are very large,
they will take longer to clone.
When it is successful,
you will get a message saying **Download Completed.**

Then you must right-click again and
click on the option called **Attacked Lines.**
There it will list the files that have already
been attacked (validated) and the ones that still need to be attack.

![Attacked lines](https://res.cloudinary.com/fluid-attacks/image/upload/v1688563519/docs/analysts/vs-code/toe-lines.png)

This table gives you the following information:

- **File name:** The Path of the file,
  where you can click and it redirects you to the file.

- **Attacked:** If the line has already been attacked,
  the value is True and False when it needs to be validated.

- **Attacked lines:** How many lines attacked.

- **LOC (Lines of Code):** How many lines of code does
  this file have in total.

- **Modified:** The last time the file was modified.

- **Comment:** Comments added from the file.

- **Sorts Priority:** Percentage of probability that
  this file has vulnerabilities.

> **Note:** Note: If you see Files that do not have the URL link,
> they are files that were previously in the repositories
> but have been removed from the repository and are no
> longer part of the project.

Selecting the File Name column will redirect you to that file,
and you can start validating.
If you find any vulnerability to report,
it is very simple,
select the line,
right-click,
and choose **Add selected text to YAML** option.

![Add YAML](https://res.cloudinary.com/fluid-attacks/image/upload/v1688563560/docs/analysts/vs-code/add_yaml.png)

By clicking on this option,
you can select a file with the YAML extension;
even if it is empty,
it will autofill the vulnerability report form.
If you want to know more about how to report vulnerabilities,
you can enter
[here.](/talent//hacking/analysts/reporting-vulns)

When opening the file,
you can see information on that vulnerability
already filled in with the fields handled.

![file filled](https://res.cloudinary.com/fluid-attacks/image/upload/v1688563634/docs/analysts/vs-code/yaml_file.png)

> **Note:** If you select several lines simultaneously,
> the display will list them all.

If you want to know in customer,
view this extension's functionality you can enter
[here.](/tech/ide/#functions)
