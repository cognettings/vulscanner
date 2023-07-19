---
slug: thinking-like-hacker/
title: Think Like a Hacker!
date: 2021-09-10
subtitle: And succeed in dealing with threat actors
category: philosophy
tags: hacking, cybersecurity, exploit, red-team, company
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1631323179/blog/thinking-like-hacker/cover_hacker.webp
alt: Photo by Giorgio Trovato on Unsplash
description: This blog post is based primarily on a study of hackers' attitudes and behaviors. These insights may help a bit in preventing attacks by threat actors.
keywords: Hacker, Thinking, Access, System, Vulnerability, Attack, Pentesting, Ethical Hacking
author: Felipe Ruiz
writer: fruiz
name: Felipe Ruiz
about1: Cybersecurity Editor
source: https://unsplash.com/photos/HAFZE_xZR4o
---

Already a decade ago, [columnist Roger A. Grimes commented as
follows](https://www.csoonline.com/article/2622041/to-beat-hackers—​you-have-to-think-like-them.html):
"Career advisers often ask me what trait would most help an IT security
pro excel. My answer is always the same: Think like a hacker." However,
he immediately clarified that he was not referring to malicious
(black-hat) hackers but to people who can devise ways to penetrate any
computer system without engaging in illegal activities (white-hat
hackers). Nevertheless, we could assume that only the motivations and
ultimate purposes may differentiate the two groups. "By looking at
systems through the eyes of a hacker, you can better identify weaknesses
and create defenses. The best antihackers are hackers themselves," said
Grimes. (In fact, this is Fluid Attacks' core, employing ethical
hackers on behalf of client companies' cybersecurity.)

Related to these observations, this time, I took as the primary
reference for this blog post [the research conducted by Esteves,
Ramalho, and de
Haro](https://sloanreview.mit.edu/article/to-improve-cybersecurity-think-like-a-hacker/),
published in 2017 in the [MIT Sloan Management
Review](https://sloanreview.mit.edu/). Basically, they surveyed 23
experienced hackers and, from the collected data, created a framework to
help organizations respond to cyberattack threats. Let’s see what we
could take away from their article and other sources.

Nowadays, we need to know that a good fight against cybersecurity risks
requires that, within the companies concerned, everyone involved
understands the traits, stratagems, and mindsets of those who can become
intruders. All these people in charge need to maintain an open and
flexible posture to see the threat actors and problems from different
angles.

Among the first characteristics of hackers (both black-hat and
white-hat) mentioned by the referenced authors, we have their high
intellectual capacity, their supporting knowledge in computer science,
and their tendency to enjoy taking risks. When it comes to malicious
hackers specifically, they are often attracted by the idea of making
thousands or millions of dollars with their cyber assaults. These
attacks can easily be directed at individuals or organizations
considerably distant from their places of action. Today, unlike in the
past, these criminals work in groups, which can undoubtedly make them
stronger. Each individual can contribute to the team with their
particular expertise and specialties.

## Mindsets and actions of hackers

Trying to think like the attacker is to act preventively. It is to want
to anticipate what the criminal can do with your systems and information
assets in order to reduce risks. For this purpose, it is pretty helpful
to know the mindsets or sets of attitudes conferred to hackers. (But,
again, these basic tendencies, far from bad intentions, can also be
attributed to ethical hackers, who can best understand threat actors.)
Precisely, Esteves and colleagues offer us two mindsets associated with
hackers in an attack: **explorative** and **exploitative**. When an
attack is just beginning, "hackers typically use an *exploration
mindset* that combines deliberate and intuitive thinking and relies on
intensive experimentation. \[…​\] Once access to a system is gained,
hackers rely on an *exploitation mindset* to meet their goals" (e.g.,
information theft).

Linked to these two previous sets of attitudes, the researchers refer to
four steps typically followed by hackers in their attacks. Two
exploration steps: (1) identifying vulnerabilities and (2) scanning and
testing. Two exploitation steps: (3) gaining access and (4) maintaining
access.

In the first step (identifying vulnerabilities), hackers tend to
demonstrate patience and determination, as well as cleverness and
curiosity. Having chosen, for example, a company as a target, they
thoroughly examine the systems for vulnerabilities. They collect as much
data as possible (i.e., *footprinting* technique). As our Offensive Team
Leader [Andres Roldan](../authors/andres-roldan) once mentioned in a
presentation, hackers (including ethical ones) obtain, for example,
technical details of the target, technical constraints, and enumeration
of possible controls and data.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/ethical-hacking/"
title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>
</div>

By detecting many of the security flaws available for exploitation,
human error often comes into the hackers' sights as well. Access to
systems can be facilitated by deceptive communication with company
insiders who may unknowingly hand over credentials to attackers. From
this, characteristics such as social and persuasive skills also stand
out in some hackers.

In the second step (scanning and testing), hackers are bent on making
progress. Their advancement with unauthorized access can be facilitated
by the vulnerabilities they detect with scanning tools in apps on the
systems. These flaws, though they may be small, can contribute to
opening an even bigger hole.

In the third step (gaining access), hackers intrude into the system
after having defined the potential vulnerability paths to follow or
exploit. As Roldan said in his presentation, hackers can use public
exploits or craft their own. They can abuse authorization flaws, crack
credentials, and gain admin-like access. From there, they exfiltrate as
much information as possible, abuse privileges, and access other domains
with lateral movement.

Then, according to the authors, in the final step (maintaining access),
"hackers try to retain their ownership of the system and access for
future attacks while remaining unnoticed." At this stage, it is common
for hackers to erase traces and evidence to avoid detection.

## How can all this help us?

All this is just a glimpse. Finding out broadly how a hacker thinks and
acts, discovering their behavior patterns, for example, by [studying
attacks that have already
occurred](https://www.darkreading.com/vulnerabilities-threats/how-to-think-like-a-hacker)
or seeing them attack (ethical hackers, of course), can incredibly
educate your firm in the field of cybersecurity. It can especially help
your engineers and developers to generate plans, prepare for possible
future events and reduce risks.

From the work of Esteves and colleagues, you can follow several
recommendations. First of all, try to get specialized individuals,
hopefully already qualified as hackers, to join your staff or work as
outsiders, who, apart from evaluating your systems, help instruct other
of your employees from an offensive standpoint. For instance, some
organizations have invited hackers to penetrate their software and
discover flaws for rewards and recognition ([bug
bounties](https://www.hackerone.com/resources/hackerone/what-are-bug-bounties-how-do-they-work-with-examples)).
Moreover, [for a long time
now](https://pctechmag.com/2011/09/how-7-black-hat-hackers-landed-legit-jobs/),
some black-hat hackers have begun to switch sides. They have been sought
out and hired to work ethically, even in companies on which they
directed attacks.

Look for ways to do footprinting in your firm on a regular basis, and go
over your systems and their weaknesses with a fine-tooth comb. Take care
to educate your employees about your data handling policies and the
techniques malicious hackers might use to deceive them. Conduct
penetration tests on your apps with the help of your experts and
companies such as Fluid Attacks to find out how far cybercriminals
could get into your systems and why. Keep an eye on all potential paths
to close or block them asap. Finally, maintain active vigilance for
suspicious events and ensure that your control and monitoring systems
remain up to date.

If you want to start immersing yourself in the ideas and ways of
thinking of hackers or broaden your spectrum in this regard, I invite
you to take a look at our posts ([1.0](../tribe-of-hackers-1/),
[2.0](../tribe-of-hackers-2/), [3.0](../tribe-of-hackers-3/),
[4.0](../tribe-of-hackers-4/), [5.0](../tribe-of-hackers-5/)) based on
the [Tribe of Hackers Red
Team](https://www.amazon.com/gp/product/B07VWHCQMR/ref=dbs_a_def_rwt_bibl_vppi_i2)
book by Carey and Jin (2019).

<quote-box>

One of the most important steps to preventing a cybersecurity breach
is understanding your adversary; the techniques they're using, the
malware they’re armed with, what they're targeting, and the
vulnerabilities that put you most at risk.
—[Threatpost](https://threatpost.com/webinars/how-to-think-like-a-threat-actor/?utm_source=TT&utm_medium=TT&utm_campaign=August_Uptycs_Webinar)

</quote-box>
