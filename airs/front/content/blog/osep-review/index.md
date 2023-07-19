---
slug: osep-review/
title: OSEP Review
date: 2023-05-04
subtitle: An OffSec Experienced Pentester review
category: opinions
tags: cybersecurity, red-team, training, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1683552579/blog/osep-review/cover_osep_review.webp
alt: Photo by Pramod Tiwari on Unsplash
description: In this post, we review the PEN-300 course and OSEP certification offered by OffSec.
keywords: OSEP, Red Team, Red Teaming, Cybersecurity Success, Security Status, Ethical Hacking, Pentesting
author: Andres Roldan
writer: aroldan
name: Andres Roldan
about1: VP of Hacking and Research
source: https://unsplash.com/photos/z16Cd-yQ-Xg
---

OSEP (OffSec Experienced Pentester) is an OffSec
(previously known as Offensive Security)
certification launched in late 2020.

It was one of the three certifications
(along with OSWE and OSED)
that appeared to conquer OSCE(3)
as a replacement for the mythical OSCE.
OSCE was way more advanced and difficult than OSCP,
but its contents,
although mostly relevant up to its final,
dated back to 2012.

The first OSEP exams were reportedly taken in January 2021,
and John Hammond was
[arguably one of the first to pass](https://www.youtube.com/watch?v=iUPyiJbN4l4&ab_channel=JohnHammond).

OSEP is about advanced Pentesting and Red Teaming techniques
and is heavily focused on creating custom tooling,
client-side abuses (Office, WSH, MSHTA),
process injection, Antivirus evasion,
advanced lateral movement (Windows/Linux)
and Active Directory attacks.

To enroll in OSEP,
you have [multiple plan choices](https://www.offsec.com/pricing/).
I used the *Course & Cert Exam Bundle*,
which allowed me to:

- Get access to the course material (written and video) for 90 days
- Download the course material once!
- Have 90 days of access to labs/challenges
- Take the exam once

As it was designed to be a replacement
for an honestly weak evasion section of the OSCE course
(Cracking The Perimeter),
OSEP can be ranked as a hard certification.
The course that prepares you
to take the certification
is called PEN-300.
Let's take a look at the summary.

## PEN-300

The official PEN-300 syllabus can be seen [here](https://www.offsec.com/courses/pen-300/download/syllabus).

The first two chapters are informative.
The first is an introduction to the course,
materials and labs,
and contains general information about the exam.
The second describes basic Windows Operating System theory,
including the Win32 API,
*WoW* (Windows on Windows) and the Windows Registry.

The next two chapters are focused on client-side attacks.
Starting with HTML smuggling and VBA basics,
the third chapter rapidly escalates on difficulty
with PowerShell download cradles,
PowerShell .NET object calling and Reflection.
The fourth chapter describes abuses of the Windows Script Host tool
that can run arbitrary code on VBScript and JScript.
As there's no known way to directly call Win32 APIs from JScript,
the fourth chapter introduces tools like DotNetToJscript and SharpShooter
that are used to accomplish this task via deserialization.

The next chapter is about Process Injection,
where different techniques are described
to inject code into another process,
including the use of Win32 APIs,
DLL Injection, and Process Hollowing.
Those techniques can be used together with the client-side attacks
described in the previous chapters,
and this is where the fun of PEN-300 starts.

Chapters five and six are related to Antivirus bypasses,
with techniques like obfuscation,
behavior bypass, sandbox detection and [AMSI bypasses](../amsi-bypass-python/).

The following chapter was my favorite,
and it's related to AppLocker bypasses.
Several techniques are described thoroughly,
including the use of custom PowerShell runspaces
and the use of client-side attacks for bypassing AppLocker rules.

There are two no consecutive chapters
(Bypassing Network Filters and Kiosk Breakups)
which are highly theoretical and too specific.
IMO,
that kind of content is more relevant in a blog post
than in a chapter of a certification book.
If they were removed from the course materials,
nothing relevant to OSEP would be lost.

The chapter Linux Post Exploitation is somewhat weak too.
A couple of abuses using VIM backdoors are described.
The only fun part was the implementation of DLL Injection,
but in the Linux realm,
using shared libraries.

Then a chapter appears
to restore the expected level of the course.
Enter Windows Credentials.
In this chapter,
the most common ways of abusing Windows Credentials are mentioned,
including *SAM* dumping,
Security Tokens manipulation, and Kerberos.
A custom `MiniDumpWriteDump()` implementation is created
to dump the *LSASS* process memory
to avoid AVs (if protections like *PPL* are not in place).

The next chapter,
Windows Lateral Movement,
is also very interesting.
Abuses of RDP are explained
beyond the obvious use of the protocol for lateral movement.
Also,
a technique called *Fileless Lateral Movement* was quite fascinating
and relevant to everyday Red Teaming engagements.

The chapter Linux Lateral Movement also describes abuses
using the SSH protocol and tools
that can be found in modern Linux servers
that are part of an on-prem DevOps infrastructure,
like Ansible and JFrog.
Also,
it mentions abuses
on how Kerberos and things
relevant to an Active Directory deployment
are relevant on a Linux-joined machine.

The next two chapters are the largest.
Microsoft SQL Attacks and Active Directory Exploitation
cover misconfigurations that can be leveraged
to escalate privileges on an AD Domain.
Although the longest,
the depth of content is nothing like that of courses
such as CRTP, CRTE, CRTO and eCPTX.
If you are expecting to master AD attacks
using only the PEN-300 content,
you may be disappointed.

Finally,
the last chapter,
Combining the Pieces,
was my second favorite.
It is a very helpful chapter
describing a sample scenario
where most of the techniques described throughout the course are employed,
which gives a glimpse of what the challenges and exam would be like.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/penetration-testing/"
title="Get started with Fluid Attacks' Penetration Testing solution
right now"
/>
</div>

## Lab

Along the way of the course contents,
there are labs on which you can practice everything that's presented.
Each lab may contain one or more machines
with different configurations and learning objectives.
You will need to use an OpenVPN client
to access the environment.
On most of the course contents,
there are exercises to practice in the lab.
You may end up with several custom tools for specific attacks.
I heavily recommend organizing it properly
because many of those tools will be used
during the challenges and even the exam
with minimal changes.
This is how I arranged the resulting artifacts during the course:

![Lab notes layout](https://res.cloudinary.com/fluid-attacks/image/upload/v1683239294/blog/osep-review/image1.webp)

## Challenges

Aside from the labs,
there are six challenges included in the PEN-300 course.
Those challenges provide an environment
where you must gather flags
on different machines to complete them.
The first four challenges are focused on specific topics of the course.
The fifth and sixth are broader in scope
and simulate very well
what the exam environment would look like.

Take notes and save any tool you create or modify
when solving the challenges.
I created a `notes.txt` file on each stage of the challenges
to use as a reference:

![Challenge notes layout](https://res.cloudinary.com/fluid-attacks/image/upload/v1683239293/blog/osep-review/image2.webp)

Therefore,
it is absolutely recommended to finish all the challenges
before attempting to take the exam.
You can thank me later.

## Exam tips

1. Finish all the challenges before attempting the exam.
   That's it. Bye.
   Jokes aside,
   this is the most important tip of all.
   If you could even solve them twice…
1. I strongly recommend taking certifications
   like CRTP or CRTO
   before attempting OSEP.
   Life will be easier.
1. Practice on HTB:
    1. Cybernetics (Prolab)
    1. Offshore (Prolab)
    1. Dante (Prolab)
    1. Hades (Endgame)
1. Join the [OffSec Discord server](https://discord.gg/offsec).
   The community is awesome,
   and OffSec support personnel can assist you with anything
   related with the course, labs, and challenges.
1. There are different exam environments.
   If you fail your attempt,
   the next retake may not be in the same environment.
   Take that into account.
1. The VPN connection is not stable.
   As it's a UDP tunnel,
   there can be problems with the *MTU* size calculation
   (VPN MTU > Link MTU),
   which can lead to packet loss during heavy traffic,
   like downloading/uploading a file to the environment,
   performing port scanning, etc.
   Follow [this guide](https://www.thegeekpub.com/271035/openvpn-mtu-finding-the-correct-settings/)
   to troubleshoot it.
   In the end,
   I had to add the `mssfix 1387` line
   to my OpenVPN connection file
   to fix those issues.

![VPN fix](https://res.cloudinary.com/fluid-attacks/image/upload/v1683239293/blog/osep-review/image3.webp)

## The bad

The course content is slightly out of date.
The last update was in 2021,
which is a very long time
for the highly dynamic world of Active Directory attacks.
Things that are not present
include ADCS abuses,
advanced coercing attacks
(MS-RPRN, MS-FSRVP, MS-EFSR aka. PetitPotam, etc.),
vulnerabilities like KrbRelayUp and ZeroLogon,
modern technologies bypass
(EDRs, ETW, ASR, WDAC, Kernel Callbacks),
GPO abuses (!),
WMI/COM,
persistence mechanisms.

Also,
the exam is proctored.
The proctoring plugin makes the computer really slow.
I used a 4k screen that made my laptop run very hot.
I had to change the resolution to 2k
to mitigate the resource consumption.

## Comparison

PEN-300/OSEP covers several things,
from evasion to Linux and Windows advanced attacks.
If you want to get comfortable with Active Directory attacks,
doing CRTP or CRTO first will give you a confidence boost.

CCRTA can give you experience attacking Linux machines
that belong to an Active Directory.

CRTL is currently more up-to-date than OSEP
in terms of bypassing techniques.
Doing it will also help you with OSEP.

Finally,
the closest certification to OSEP would be eCPTXv2.
The main difference is that OSEP includes Linux attacks,
and eCPTXv2 goes very deep on Active Directory abuses.

## Conclusions

PEN-300 is a high-quality course.
Aside from a couple of chapters,
every module had very rich, relevant and deep technical information.
The course needs an update.
Major abuses and attacks have been discovered
since the last update,
and many others presented on the course are no longer working
with today's default defenses.
In the end,
the OSEP certification will boost your Pentesting skills
to a whole new level.
