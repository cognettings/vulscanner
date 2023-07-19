---
slug: cyberattacks-2021/
title: Remembering Cyberattacks of 2021
date: 2021-12-02
subtitle: Here's what happened this year, in case you missed it
category: attacks
tags: cybersecurity, software, vulnerability, company, exploit, credential
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1638463448/blog/cyberattacks-2021/cover_cyberattacks.webp
alt: Photo by Anil Xavier on Unsplash
description: 'Supply chain attacks, ransomware and data leaks: We give you a short summary of the major cyberattacks of 2021.'
keywords: Supply Chain Attack, Ransomware, Leak, Trends, Solarwinds, Software, Darkside, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/TI45iWO9x-g
---

In case you were living under a rock
and missed all the important stuff that happened this year:
Don't worry,
we've got your back.
Of course,
we also welcome regular readers
who want to get their daily fix of cybersecurity.

## Supply chain attacks

Let's start from the beginning of the year.
The first memorable event everyone was talking about in January
was the [SolarWinds](../solarwinds-attack/) supply chain attack.
About 18,000 organizations,
including federal agencies and Fortune 500 companies,
were affected
as threat actors pushed malware in an update of SolarWinds' Orion software.
Even though this update was distributed in the first half of 2020,
it was only in December that FireEye, a cybersecurity company, detected
that attackers had found a way in
and were looking through things.
Some sources [suspected](https://www.reuters.com/article/us-usa-cyber-amazon-com-exclsuive-idUSKBN28N0PG)
that the attack was part of a cyberespionage campaign
by Russian threat actors.
However,
it seems
that at least one more group of [another nationality](https://www.reuters.com/article/us-cyber-solarwinds-china/exclusive-suspected-chinese-hackers-used-solarwinds-bug-to-spy-on-u-s-payroll-agency-sources-idUSKBN2A22K8)
was also involved.

An even bigger incident gained attention in March,
this time affecting [Microsoft Exchange Server](../exchange-server-hack/)
(MES) users.
This software is a platform
that manages email, messaging, calendaring and other collaboration utilities.
What happened is [several](https://www.checkpoint.com/downloads/resources/cyber-attack-trends-report-mid-year-2021.pdf)
threat groups exploited four zero-day vulnerabilities in MES
that allowed them to infiltrate systems,
steal data
and install backdoors for continued access and control.
Shockingly,
there were about 30,000 victim organizations in the U.S. alone,
and globally there were about 60,000.
Even though signs of compromise could be [traced back](https://us-cert.cisa.gov/ncas/current-activity/2021/03/04/update-alert-mitigating-microsoft-exchange-server-vulnerabilities)
to as early as September last year,
it was again a cybersecurity firm (Volexity)
that [detected](https://www.volexity.com/blog/2021/03/02/active-exploitation-of-microsoft-exchange-zero-day-vulnerabilities/)
anomalous activity last January.

## Ransomware, ransomware, ransomware

Also in March,
a ransomware attack targeted the U.S. insurance company CNA Financial.
It was [reported](https://www.bleepingcomputer.com/news/security/ransomware-gang-breached-cna-s-network-via-fake-browser-update/)
that cybercriminals of a gang called Phoenix breached CNA's network
thanks to their fooling an employee to install a malicious browser update.
They exfiltrated sensitive information
and "encrypted more than 15,000 devices."
The company ended up paying cybercriminals [$40M](https://www.zdnet.com/article/us-insurance-giant-cna-financial-paid-40-million-ransom-to-wrestle-back-control-of-systems/)
to regain control of its network!
This large sum set a record among known ransomware payments.
Thankfully,
the MEGAsync account where Phoenix collected the data was seized by the FBI
and Mega.
Most importantly,
CNA said the stolen data had not gone anywhere outside that account.

Next,
what could be considered as the [most important](https://gizmodo.com/the-biggest-hacks-of-2021-so-far-1847157024/slides/5)
cyberattack this year
was the one that hit Colonial Pipeline.
The FBI [confirmed](https://www.fbi.gov/news/pressrel/press-releases/fbi-statement-on-network-disruption-at-colonial-pipeline)
that on May 7
the networks of the longest pipeline system for refined oil products
in the U.S.
had been attacked with ransomware.
[During](https://www.checkpoint.com/downloads/resources/cyber-attack-trends-report-mid-year-2021.pdf)
the investigation of the incident,
the distribution processes were interrupted,
which meant transportation fuel shortages across the East Coast
and changes in oil prices globally.
In order to resume operations,
the company paid a [$4.4M ransom](https://www.zdnet.com/article/colonial-pipeline-ceo-paying-darkside-ransom-was-the-right-thing-to-do-for-the-country/)
to [DarkSide](../pipeline-ransomware-darkside/),
the ransomware gang behind the attack.
The U.S. government's response added to this attack's significance.
Within days,
the White House released an [executive order](https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/)
"on improving the nation's cybersecurity,"
and the gang [announced](https://www.washingtonpost.com/technology/2021/05/14/darkside-ransomware-shutting-down/)
they were ceasing their RaaS operations
"due to the pressure from the US."
Impressively,
not long after,
the Department of Justice [seized $2.3M](https://www.justice.gov/opa/pr/department-justice-seizes-23-million-cryptocurrency-paid-ransomware-extortionists-darkside)
in cryptocurrency from the ransom paid to DarkSide.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/penetration-testing/"
title="Get started with Fluid Attacks' Penetration Testing solution
right now"
/>
</div>

In late May,
JBS Foods,
the world's largest meat supplier,
[was attacked](../jbs-revil-cyberattack/) with ransomware.
As a consequence,
operations were shut down [for a few days](https://www.cshub.com/attacks/articles/iotw-jbs-recovers-quickly-from-a-ransomware-attack)
in Australia, Canada, the U.S. and other countries.
This attack was performed by REvil,
which was one of the [most well-known](https://www.zdnet.com/article/the-ransomware-landscape-is-more-crowded-than-you-think/)
ransomware operators.
JBS had to pay a [ransom of $11M](https://www.bbc.com/news/business-57423008)
to put an end to the attack.
Strikingly,
some weeks after this incident
and just hours before the beginning of the Fourth of July weekend,
REvil [attacked Kaseya](https://www.zdnet.com/article/updated-kaseya-ransomware-attack-faq-what-we-know-now/),
a Miami-based IT solutions provider.
The attack affected an estimate of 800 to 1,500 businesses
that were using a program for remote monitoring and management
developed by Kaseya.
This was another major supply chain attack,
where ransomware was deployed along with a software update.
REvil got greedy and demanded that Kaseya [pay $70M](https://www.zdnet.com/article/kaseya-denies-paying-ransom-for-decryptor-refuses-comment-on-nda/)
for decryption.
But Kaseya said they didn't pay
and used a universal decryptor they obtained from a third party instead.
Surprisingly,
on July 13,
the REvil ransomware servers [disappeared suddenly](https://www.bbc.com/news/technology-57826851)
from the dark web and the regular web.
[Reportedly](https://therecord.media/revil-gang-shuts-down-for-the-second-time-after-its-tor-servers-were-hacked/),
the group's leader took down the servers and ran away with the group's money.
The remaining members reappeared on September 7,
only for their servers to be shut down again in October,
this time by a coalition of law enforcement agencies.

## Your data for the taking

In September,
[Anonymous leaked](../epik-hack/) a database of 15M accounts
that it got from breaching domain registrar and web host Epik.
The leaked data comprised not only the website owners' credentials
but also their physical addresses and phone numbers,
among other sensitive information.
The most recent files in that database were dated February 2021
which suggests
that Epik's security vulnerability had been exploited months before the leak.
But Epik wasn't the only web host to be attacked this year.
In November,
[GoDaddy](https://threatpost.com/godaddys-latest-breach-customers/176530/),
which hosts more than 5M websites,
stated that attackers gained access in September
and were lurking inside all that time.
According to GoDaddy's Chief Information Security Officer
the breach was possible due to a compromised password.
The data to which attackers got access included usernames,
passwords and SSL private keys.
These last ones are pretty sensitive,
since they may allow threat actors to hijack a web domain
and extort the owners.
At the time of writing the present post,
an investigation is ongoing.

Lastly,
let's not forget another major leak that occurred in October.
[Twitch](https://therecord.media/twitch-source-code-and-business-data-leaked-on-4chan/),
a well-known live streaming platform,
got its source code and business data leaked.
The threat actor published a 125GB torrent containing folders
that included streamers' identities and payout data.
But among the most sensitive information
were Twitch's "authentication mechanisms,
admin management tools,
and data from [its] internal security team."
For example,
their threat models have been made public.
These are used to describe likely threat actors and how they could attack.
Twitch [stated](https://blog.twitch.tv/en/2021/10/15/updates-on-the-twitch-security-incident/)
that the leaker got their way in by exploiting an error
in a server configuration change.

## Don't let your guard down!

There you have it.
The cyberattacks mentioned here definitely show
the importance of some of the issues we've talked about in previous posts.
We have [said](../close-invisible-doors/) it's essential
to be aware of your software components' vulnerabilities.
Keeping a watchful eye and requesting Fluid Attacks' [services](../../services/continuous-hacking/)
can certainly help you stop ignoring your software's security flaws.
We have also [informed](../social-engineering/) about the weapons of influence
that criminals use to phish people into installing malware
in their company's systems.
We recommend you read that post
to be one step ahead of ransomware attacks.
Finally,
it may seem very hard to prevent leaks.
However,
we [ask](../owasp-top-10-2021/)
that you take the dangers of broken access control
and cryptographic failures seriously.
They are the riskiest security flaws in web apps,
according to the OWASP Top 10,
and seem to facilitate leaks.
In short,
every organization needs to have properly configured access restrictions
and authentication mechanisms,
and use modern encryption methods.

So,
don't let your guard down this holiday season
and take security measures right now!
