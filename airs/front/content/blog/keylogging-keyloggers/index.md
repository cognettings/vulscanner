---
slug: keylogging-keyloggers/
title: I've Seen What You Type
date: 2023-05-31
subtitle: Watch out for keylogging/keyloggers
category: attacks
tags: malware, social-engineering, cybersecurity, credential, hacking, trend
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1685588279/blog/keylogging-keyloggers/cover_keylogging_keyloggers.webp
alt: Photo by Pierre Bamin on Unsplash
description: Here we spell out what keylogging is and what keyloggers are, as well as how you can prevent, identify and remove them.
keywords: Keylogging, Keylogger, Software Based Keylogger, Hardware Based Keylogger, Kernel Level, Api Level, Spyware, Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/uu_Uh55fK24
---

I'm not behind you.
I haven't installed a camera in your room or your workplace.
Still,
I can see what you've been typing lately
on the device you're using to read this.

As much as it sounds like a fictional movie,
those words above could be rightly ascribed
to someone doing keylogging on your device.
Although,
depending on different factors,
keylogging may be legal,
it often turns out to be illegal.
As it is a serious cybersecurity risk today,
it is wise for you to know what it is
and what you can do about it.

## What is keylogging?

Keylogging is short for keystroke logging,
also often named keyboard capturing.
As the name suggests,
keylogging is the act of recording a user's keystrokes
on the keyboard of a computing device.
This process is carried out by a keylogger.
Sometimes the user of the target device is aware
that their keyboard use is being monitored
but many other times they are not.

Legitimate keylogging is often performed
to monitor computer usage and compliance with security protocols in a company
and to detect issues faced by users of a technology product
and then repair them to improve their experience.
It is also employed to investigate writing patterns,
conduct cybersecurity assessments with ethical hacking,
and even for parents to keep an eye on their underage children's Internet use.
In such cases,
there is usually consent from the device user
and no intention of the keylogger owner to misuse the recorded information.
When neither of these conditions is present
and local laws on privacy and data use are violated,
we can talk about dishonest keylogging.

## What is a keylogger?

A keylogger or keystroke recorder is a hardware or software-based tool
that allows keylogging on devices
such as computers and smartphones.
The data recorded by a keylogger can be stored in different ways
and sent,
even in disguise,
to the tool's owner
regularly through various means.
Some keyloggers can be programmed
to specifically monitor certain keystrokes,
such as the "@,"
which may indicate that
the user will enter a password immediately afterward
(something that saves a hacker time and effort).

The genesis of these tools is usually dated back to the 1970s.
The first keyloggers were created by Soviet Union intelligence,
[presumably, the KGB](https://medium.com/illumination-curated/three-cybersecurity-lessons-from-a-1970s-kgb-key-logger-895fdc96b9f6),
to be installed in IBM Selectric typewriters of U.S. government entities
in Moscow and Leningrad
(i.e., St. Petersburg).
These hardware-based keyloggers were hidden in some typewriters.
[They measured](https://www.techtarget.com/searchsecurity/definition/keylogger)
the magnetic fields from the printheads
and sent [the keystroke information](https://www.csoonline.com/article/3326304/keyloggers-explained-how-attackers-record-computer-inputs.html)
to the spies
via radio bursts.
Astonishingly,
it was not until 1984
that a U.S. ally detected their use.
Incidentally,
a year earlier,
graduate student Perry Kivolowitz developed the first software-based keylogger.
It was in the 1990s that these tools began to spread widely.

## What are the types of keyloggers?

### Hardware-based keyloggers

These are physical tools
that are attached to or installed on target devices.
For instance,
some keyloggers are placed between the keyboard connector
and the port on the computer.
They store the keystrokes in their own memories
and are usually not dependent on attached software,
something that makes them undetectable by programs such as antivirus.
There are also keyloggers based on USB connectors
that capture communications via Bluetooth
and those installed inside the keyboards themselves
so as not to be easily visible.

Similar to the latter are keyboard overlays
or keyloggers that are placed on top of ATMs
—looking like integrated parts of the machine—
to capture bank users' PINs.
Another recent and somewhat bizarre example is acoustic keyloggers.
[These are said](https://www.csoonline.com/article/3326304/keyloggers-explained-how-attackers-record-computer-inputs.html)
to monitor the sounds emitted
when someone is typing on a computer keyboard
and recognize subtle acoustic differences
that are then accurately associated with the keys pressed.

### Software-based keyloggers

These are apps or programs
that are installed on the target devices.
Mainly there are API-level and kernel-level keyloggers.
An API-level or user-mode keylogger works
as if it were a standard program inside a system,
and what it does is [hook keyboard APIs](https://www.researchgate.net/publication/318228591_The_strange_world_of_keyloggers_-_an_overview_Part_I)
inside running applications.
It intercepts the signals emitted by the keyboard
that pass through application programming interfaces (APIs)
that allow apps to receive such inputs.
On the other hand,
a kernel-level keylogger is more complex to elaborate
(so it is less common),
detect and eradicate.
It is usually implemented as a [rootkit](https://en.wikipedia.org/wiki/Rootkit)
(gaining root access),
has administrative privileges,
hides among other OS processes,
and intercepts keystrokes that pass through the [kernel](https://en.wikipedia.org/wiki/Kernel_(operating_system)),
acting as a keyboard device driver.

Among the software-based keyloggers,
JavaScript-based and form-grabbing-based keyloggers are [also often mentioned](https://www.researchgate.net/publication/318228591_The_strange_world_of_keyloggers_-_an_overview_Part_I).
The former is written in JavaScript
and injected into websites
to record keystrokes from them specifically.
The latter is aimed at capturing the information
that a user enters and submits in a web form
before reaching its recipient.

The classification of keyloggers becomes blurred
when we start talking about keyloggers
capturing more than just keystrokes.
For example,
some tools take screenshots of the target device's screen
on a regular basis.
So, to refer to them,
it might be preferable to talk about screen scrapers or screen recorders.
There are also tools that record everything
that the user copies or cuts
and that is temporarily stored in the clipboard of their device.
Even further away from the initial classification are those
that record audio, camera captures and GPS data.

However,
what perhaps allows all of these
to continue to be categorized as keyloggers
is that many have evolved in features
to include the capture of information
such as the aforementioned
*in addition* to that coming from the keyboard.
Nevertheless,
in these cases,
it would be better to call them by more general names,
such as spyware
(with negative connotations)
or device monitoring apps
(with positive connotations).

## How to prevent keylogging?

What we hope to prevent,
naturally,
is malicious keylogging,
in which criminals typically seek to steal sensitive information from victims
to sell or use for profit
(not to mention stalking or voyeurism).
For illegal keylogging,
software-based keyloggers are often spread through social engineering attacks
and are ["one of the most](https://www.csoonline.com/article/3326304/keyloggers-explained-how-attackers-record-computer-inputs.html)
common malware payloads delivered by worms,
viruses, and Trojans."
Therefore,
prevention recommendations for this particular risk can be all but the same
as those given for dealing with social engineering in general:

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/security-testing/"
title="Get started with Fluid Attacks' Security Testing solution right now"
/>
</div>

- Do not follow links in suspicious, strange or poorly written messages
  received via email or SMS.

- Do not download files of dubious provenance,
  i.e., from untrusted or unknown sites.

- Avoid using public devices and networks,
  especially for accessing and transmitting sensitive information.

- Keep a good antivirus, firewalls activated,
  and operating systems and applications updated
  to their latest versions on your device.

- [Use a password manager](../password-manager-hacked/).
  It securely stores all your passwords
  and can automatically fill in your login credentials in your apps.
  The problem is that you must type your master password
  each time you use it.
  Hence the importance of the following two recommendations.

- Enable multi-factor authentication,
  either in the password manager or in each app,
  which normally requires verification on another of your devices.

- Although it would not apply to the most advanced keyloggers or spyware
  that steal other types of data,
  when entering sensitive information in your computer,
  such as your master password,
  it may be helpful to use the virtual keyboard.

## How to identify and remove keyloggers?

In cybersecurity,
as we at Fluid Attacks recognize and advocate,
prevention should be more important
or a higher priority than response.
However,
suppose you have already been affected by a software-based keylogger.
In that case,
you may have experienced sudden manifestations of strange or abnormal behavior
on your device
and should get to work addressing the situation.
(A hardware-based keylogger attack is more unusual,
but it is not a bad idea to check your computer frequently
to ensure that there are no additional small devices
attached to it unknown to you.)
But beware;
these signs tend to suggest
only the presence and activity of keylogging malware
(or some other malicious software)
that is shoddy coded or not very advanced:

- A slowdown of device performance
  when opening and running a browser or other application.

- Pop-up windows,
  error messages and interference in loading websites.

- New icons on the desktop or in system trays.

- Lags when typing on the keyboard or moving the mouse
  (a sign closely linked to a keylogger).

- Degraded screenshots on smartphones.

Finally,
for the actual identification and removal of keyloggers,
keep the following recommendations in mind:

- Especially **for API-based keyloggers**,
  take an inventory of the software inside the device
  (including browser extensions)
  to find out if there are any you know you have never downloaded
  or are unfamiliar with.

- Related to the above,
  you should examine the device's task manager
  to see which programs are running by default
  (from the device boot-up)
  or at certain times,
  such as when you are about to type sensitive information.

- Check which files are being updated frequently,
  something that could indicate the continuous recording of new information.

- Once the suspicious programs have been detected,
  the idea is to look for information about them
  and verify what they are in order to remove them
  (in some cases, it'd be necessary to reformat the device).

- **For kernel-based keyloggers**,
  you require programs such as antivirus software
  that are advanced enough to scan for rootkit-like behavior.

- You can also resort specifically to anti-keylogger software.
  On the one hand,
  these tools can encrypt keystrokes at the kernel level
  so that they are read only by the expected,
  legitimate application.
  On the other hand,
  they can perform detection scans
  by comparing databases of known keyloggers
  with the files of the device under evaluation.
  They can even warn you of keylogging behavior on your devices.
  Once keyloggers are identified,
  they can be removed.
