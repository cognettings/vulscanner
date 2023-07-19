---
slug: argentina-leak/
title: A Whole Nation Compromised
date: 2021-11-05
subtitle: All of Argentina's population IDs stolen and for sale?
category: attacks
tags: cybersecurity, vulnerability, exploit, credential
image: https://res.cloudinary.com/fluid-attacks/image/upload/v1636118998/blog/argentina-leak/cover_argentina.webp
alt: Photo by Chaos Soccer Gear on Unsplash
description: This new leak may compromise more than 45M people. Read this post to learn who the attacker is, how he gained access and his connection with past leaks.
keywords: Argentina, IDs, RENAPER, Messi, Gorra, Leak, Stolen, Ethical Hacking, Pentesting
author: Jason Chavarría
writer: jchavarria
name: Jason Chavarría
about1: Cybersecurity Editor
source: https://unsplash.com/photos/Cjfl8r_eYxY
---

No day passes without cybersecurity incidents.
Too often,
we read shocking headlines about massive leaks.
Last month
we learned that a person claimed
to have stolen personally identifiable information
from **the entire population of Argentina**
and is currently selling all this data.
Enough time has passed since this early claim
so that reporters have got ahold of the alleged threat actor.
Reportedly,
it may be true that they have the entire database,
which means more than 45M people may be compromised.
Not only that,
but apparently this same individual
was involved in previous notable leaks in the country.

## Data of more than 45M compromised

Initially,
the new leak got public attention
as someone under the handle @aniballeaks published
the national ID card photos
and Trámite number
of at least 44 Argentine public figures on Twitter.
Among those whose information was compromised were
famous soccer players Lionel Messi and Sergio Aguero,
but also the president of Argentina,
Alberto Fernández.
That Twitter handle is a variation
of the one used in a
[previous leak](https://www.clarin.com/tecnologia/filtraron-informacion-privada-miembros-fuerzas-armadas-seguridad-argentina_0_R5nYFK-2E.html)
in September (we’ll get to that),
which was chosen as a taunt
to Argentina’s Minister of Security Aníbal Fernández.
The account @aniballeaks is now
[suspended](https://www.zdnet.com/article/twitter-suspends-hacker-who-stole-data-of-46-million-argentinians/).
Argentine security researcher Javier Smaldone
[suspected](https://twitter.com/mis2centavos/status/1447251622334275595)
early on
that the photos were
most probably from the National Registry of Persons
(RENAPER in Spanish).
He was later proven right.

On October 10,
the threat actor posted in a well-known hacking forum,
[offering to sell](https://therecord.media/hacker-steals-government-id-database-for-argentinas-entire-population/)
"all the data in the national identity document (DNI)
of any person in Argentina."
The stolen database contains names,
home addresses,
birthdays,
Trámite numbers,
citizen numbers,
government photo IDs,
labor identification codes,
ID card issuance
and expiration dates.
Out of these,
the most sensitive seems to be the Trámite numbers.
This number is asked by various institutions
to concede personal loans
or to complete remote transactions.

<div class="imgblock">

![Forum post](https://res.cloudinary.com/fluid-attacks/image/upload/v1636119134/blog/argentina-leak/argentina_figure_1.webp)

<div class="title">

Figure 1. Forum post where data is being offered for sale. Source: [therecord.com](https://therecord.media/wp-content/uploads/2021/10/Argentina-DB.png).

</div>

</div>

It was only on October 13
that the Ministry of Interior issued an
[official statement](https://www.argentina.gob.ar/noticias/el-renaper-detecto-el-uso-indebido-de-una-clave-otorgada-un-organismo-publico-y-formalizo)
confirming that the images were taken from the RENAPER.
In this statement,
it was informed
that credentials assigned to the Ministry of Health were used
for leaking images
pertaining to the national identity documents.
(Many institutions,
such as the Ministries of Health,
Transport
and Security,
rely on the RENAPER for identity validation purposes.)
It was also informed
that the RENAPER cybersecurity team was able to determine
that 19 of the images had been consulted
at the same time they were being posted on Twitter.
But also,
according to the specialists,
the incident was not a result of unauthorized access
and there was no massive leak.
Yikes\!
What was found later proved that was not the case.

<div>
<cta-banner
buttontxt="Read more"
link="/solutions/ethical-hacking/"
title="Get started with Fluid Attacks' Ethical Hacking solution right now"
/>
</div>

## And the attacker’s name is…​

In late October,
the threat actor
(at this time,
we will have to assume it’s the same person)
gave some interviews for some media outlets.
In an [interview](https://therecord.media/hacker-steals-government-id-database-for-argentinas-entire-population/)
for The Record
on October 18,
the interviewee confirmed
that they have the personal information of every Argentine.
To prove it,
the individual provided
the personal details of an Argentine citizen of The Record’s choosing.
That personal information included the Trámite number.

In a more recent
[interview](https://www.rosario3.com/tecnologia/El-robo-del-siglo-una-reveladora-entrevista-a-S-el-enigmatico-e-indetectable-hacker-del-Renaper-20211027-0050.html)
for local news site Rosario3 on October 27,
the interviewee went by the name "\[S\]."
This name has been linked to two past breach incidents
known as
"[La Gorra Leaks](https://www.zdnet.com/article/argentinian-security-researcher-arrested-after-tweeting-about-government-hack/)
1.0 and 2.0."
The first breach happened in 2017
when the Twitter account of Patricia Bullrich,
then Minister of Security of Argentina,
and that of the Airport Security Police were hacked.
The second breach was in August 2019
and involved thousands of files
that "contained names, surnames,
ID numbers, home addresses,
telephone numbers,
and banking information for \[Argentine\] Federal Police officers."
(Apparently,
several people were responsible for this last breach,
seeing as two suspects were eventually arrested.)
In addition to these incidents,
\[S\] is also linked to the previous "AnibalLeaks,"
which happened
[last September](https://www.clarin.com/tecnologia/filtraron-informacion-privada-miembros-fuerzas-armadas-seguridad-argentina_0_R5nYFK-2E.html).
\[S\] leaked the personal
and contact information for almost 1.2M members of the Security Forces
and Armed Forces of the Argentine Republic.

So,
back to the interview.
From \[S\]'s responses,
it can be suggested that he identifies as male.
Further,
\[S\] revealed he is a software developer
who is involved in cybercrime just as a hobby.
He explained
that he accessed the RENAPER database using valid credentials,
which,
according to him,
are available for purchase.
So as to not raise any suspicion,
he downloaded information
alternating between different credentials.
Further,
he admitted to having sold the entire database six times
within the week of the interview and the one preceding it.
By the way,
its price is 0.29 BTC,
which equals about 17,700 USD
by the time of this entry.
As a way to avoid leaving traces with cryptocurrency transfers,
he exchanged Bitcoins for
[Monero](https://www.getmonero.org/resources/about/)
(XMR).
He says it’s impossible to catch him.

## Argentina, hammered

In the latter interview,
\[S\] says he expects
the entire database will be in circulation
in a matter of months.
Now,
Argentine citizens are open to all kinds of scams,
the most threatening being financial fraud.
\[S\] mentioned
that maybe this would make people aware
that their government is not safeguarding their personal data.
Indeed,
this also needs to be a warning
to every country’s government.
They need to take every precaution,
keeping the mentality
that any day they may be breached.
