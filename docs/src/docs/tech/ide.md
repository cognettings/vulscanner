---
id: ide
title: IDE Extension
sidebar_label: IDE Extension
slug: /tech/ide
---

`Fluid Attacks'` has an extension in the
**Visual Studio Code (VScode)** editor.
With this extension,
you can see reported vulnerabilities in the
[platform](/tech/platform/introduction)
where pointing you to the specific file
and line of code where the vulnerability was
reported and redirect you to
[criteria](/criteria/vulnerabilities/)
documentation.
Remember that depending on the files you
have as analysis input,
these are the ones that will reflect this information.

## Download extension

To download the extension,
go to the extension section,
and type **Fluid Attacks** in the search bar.

![Find extension](https://res.cloudinary.com/fluid-attacks/image/upload/v1680090457/docs/machine/vscode-extension/find_the_extension.png)

## Configure the editor with Fluid Attacks' platform

Once you have downloaded the extension,
it is necessary to configure it to connect
the platform with your editor.
Go to **configuration => settings**.

![settings](https://res.cloudinary.com/fluid-attacks/image/upload/v1680090891/docs/machine/vscode-extension/setup-settings.png)

In the search bar,
enter the name of the **Fluid Attacks** extension;
there,
you must enter your platform
[API token](/tech/api/#authentication-with-the-fluid-attacks'-platform-api-token)
once you have entered it,
close and reopen your editor to update this change.

![Platform api token](https://res.cloudinary.com/fluid-attacks/image/upload/v1680097089/docs/machine/vscode-extension/arm_token.png)

## Functions

Once you have the extension and the configuration,
you can use this tool.
The functions you will find in this tool are:

- Pointing out the
  [file and the line](/tech/ide/#file-and-code-line-pointing)
  of code with vulnerability.

- [Redirecting](/tech/ide/#redirection-to-the-fluid-attacks-platform-platform)
  that vulnerability to Fluid Attacks' platform.

- Applying the Temporarily accepted treatment.

- Going to
  [criteria](/tech/ide/#go-to-criteria).

- [Request reattack](/tech/ide/#request-reattack).

### File and code line pointing

To visualize the **vulnerabilities** reported
in Fluid Attacks' platform from the editor,
you have to open the project in which it
is active in the vulnerability analysis.
You can detect the files since they have
red dots or open them directly by file
line by clicking on the **X symbol**.

![visualize vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1680092660/docs/machine/vscode-extension/visualize_vuln.png)

You will see a list of vulnerabilities
where you will be redirected to the file and the vulnerable line of code.

![line vulnerabilities](https://res.cloudinary.com/fluid-attacks/image/upload/v1680092726/docs/machine/vscode-extension/vuln_line.png)

### Redirection to Fluid Attacks' platform

Once you have the line of code where the vulnerability is reported,
put the cursor of your mouse over it,
and you will get a pop-up window where it will give
you the definition and the redirection link.

![redirection platform](https://res.cloudinary.com/fluid-attacks/image/upload/v1680094385/docs/machine/vscode-extension/redirection_arm.png)

Clicking on the link will open Fluid Attacks' platform
where this reported
[vulnerability](/tech/platform/vulnerabilities/management/locations)
is located.

### Temporarily accepted treatment

You can apply the **Accept Vulnerability Temporary treatment**
by right-clicking on the line of code.

![Accepted treatment](https://res.cloudinary.com/fluid-attacks/image/upload/v1680094538/docs/machine/vscode-extension/accepted_treatment.png)

There you put the justification and the date of the treatment application.

### Go to criteria

Clicking on [criteria](/criteria/vulnerabilities/)
will take you to the documentation.

![Go criteria](https://res.cloudinary.com/fluid-attacks/image/upload/v1680094653/docs/machine/vscode-extension/criteria.png)

### Request reattack

You can also request a [reattack](/tech/platform/reattacks)
by clicking on this one,
where you will put the justification.

![reattak](https://res.cloudinary.com/fluid-attacks/image/upload/v1680094913/docs/machine/vscode-extension/request.png)

## Troubleshooting

If some repositories are not detected when downloading the extension,
you have to go to the settings section of the **Fluid Attacks**
extension and add the groups that are part of it.

![Fluid Attacks settings](https://res.cloudinary.com/fluid-attacks/image/upload/v1680710031/docs/machine/vscode-extension/fluid_settings.png)

There you will click where it says Edit in **settings.json**.

![settings json](https://res.cloudinary.com/fluid-attacks/image/upload/v1680710198/docs/machine/vscode-extension/settings_json.png)

It will open a **.json** file where you can add the groups
where those repositories are not activated.

![add groups](https://res.cloudinary.com/fluid-attacks/image/upload/v1680710264/docs/machine/vscode-extension/adding_groups.png)
